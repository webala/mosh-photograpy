from django.shortcuts import  render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from dashboard.serializers import MyMessageSerializer, SetShootCompleteSerializer, ImageActionSerializer
from shop.forms import MessageForm, MyMessageForm
from shop.models import Client, Message, MyMessage, Package, Shoot, Transaction, GalleryImage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import message_data, shoot_data
from shop.utils import send_email

# Create your views here.


def register_user(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        print("saved user: ", user)
        return redirect("login")

    context = {"form": form}

    return render(request, "registration/register.html", context)


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            associated_user = User.objects.filter(email=email).first()
            if associated_user:
                subject = "Password Reset Requested"
                email_template_name = "registration/password_reset_email.txt"
                email_context = {
                    "email": associated_user.email,
                    "domain": "localhost:8000",
                    "site_name": "Glitch Cloud",
                    "uid": urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    "user": associated_user,
                    "token": default_token_generator.make_token(associated_user),
                    "protocol": "http",
                }
                email = render_to_string(email_template_name, email_context)
                try:
                    send_mail(
                        subject,
                        email,
                        "webdspam@gmail.com",
                        [associated_user.email],
                        fail_silently=False,
                    )
                except BadHeaderError:
                    return HttpResponse("Invalid header found.")

                return redirect("password-reset-done")
    form = PasswordResetForm()
    return render(request, "registration/password_reset.html", context={"form": form})


@login_required
def dashboard(request):
    shootData = shoot_data()
    messageData = message_data()
    clients = len(list(Client.objects.all()))
    packages = len(list(Package.objects.all()))
    gallery = len(list(GalleryImage.objects.all()))
    context = {
        "shoot_data": shootData,
        'message_data': messageData,
        'clients': clients,
        'packages': packages,
        'gallery': gallery
    }

    return render(request, "dashboard.html", context)


def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')

def message_create(request):
    form = MessageForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Message sent successfully")
        return redirect("home")
    else:
        messages.error(request, "Message not sent. Please check your inputs.")
        return redirect("home")



class TransactionsList(LoginRequiredMixin, ListView):
    model = Transaction
    template_name: str = "transactions.html"
    context_object_name: str = "transactions"
    paginate_by: int = 10


class MessagesList(LoginRequiredMixin, ListView):
    model = Message
    template_name: str = "messages.html"
    context_object_name: str = "client_messages"
    paginate_by: int = 10
    ordering = ['-id']


class ShootsList(LoginRequiredMixin, ListView):
    model = Shoot
    template_name: str = "shoots.html"
    context_object_name: str = "shoots"
    paginate_by: int = 10


class ShootDetail(LoginRequiredMixin, DetailView):
    model = Shoot
    template_name: str = "shoot.html"
    context_object_name: str = "shoot"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shoot = super().get_object()
        packages = shoot.package.all()
        context["packages"] = packages
        return context


class TransactionDetail(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name: str = "transaction.html"
    context_object_name: str = "transaction"


class ClientDetail(LoginRequiredMixin, DetailView):
    model = Client
    template_name: str = "client.html"
    context_object_name: str = "client"


class ClientList(LoginRequiredMixin, ListView):
    model = Client
    template_name: str = "clients.html"
    context_object_name: str = "clients"
    paginate_by: int = 15


class MessageDetail(LoginRequiredMixin, DetailView):
    model = Message
    template_name: str = "message.html"
    context_object_name: str = "client_message"


    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        message = super().get_object()
        replies = MyMessage.objects.filter(replied_message=message)
        context['replies'] = replies
        reply_form = MyMessageForm()
        context['form'] = reply_form
        return context

    
    def get_object(self, queryset=None):
        message =  super().get_object(queryset)
        if not message.read:
            message.read = True
            message.save()
        
        return message


@api_view(["POST"])
def set_shoot_complete(request):   
    serializer = SetShootCompleteSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        shoot_id = data.get('shoot_id')
        complete = data.get('complete')

        query = Shoot.objects.filter(id=shoot_id)
        if query.exists():
            shoot = query.first()
            shoot.complete = complete
            shoot.save()
            return Response({'message: ': 'Shoot complete status changed'})
        else:
            return Response({'message: ': 'Shoot does not exist'})
        

@api_view(['POST'])
def send_my_message(request):
    serializer = MyMessageSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        replied_message_id = serializer.validated_data.get('message_id')
        message = serializer.validated_data.get('my_message')
        query = Message.objects.filter(id=replied_message_id)
        if query.exists():
            replied_message = query.first()
            reply = MyMessage.objects.create(
                replied_message=replied_message,
                message=message
            )
            receiver = replied_message.email
            send_email(replied_message.message, message, receiver)
            return Response({'message': 'Message sent.'}, 200)
        else:
            return Response({"message": "Message does not exist"}, 404)
    
@login_required
def dashboard_gallery(request):
    gallery_images = GalleryImage.objects.all()
    context = {
        'gallery_images': gallery_images
    }
    return render(request, 'dash_gallery.html', context)

@api_view(['POST'])
def image_action(request):
    serializer = ImageActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        photo_id = data.get('photo_id')
        action = data.get('action')
        photo = GalleryImage.objects.get(id=photo_id)
        if action == 'delete':
            photo.delete()
            return Response({'message': 'Photo deleted'}, 200)
        elif action == 'display':
            photo.display = not photo.display
            photo.save()
            return Response({'message': 'Photo display changed'}, 200)
    else:
        return Response({'message': 'Invalid id or action'}, 400)
