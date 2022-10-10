from django.shortcuts import HttpResponse, render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from dashboard.serializers import MyMessageSerializer, SetShootCompleteSerializer
from shop.forms import MessageForm
from shop.models import Client, Message, Package, Shoot, Transaction
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

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

# class PasswordResetConfirm(PasswordResetConfirmView):
#     success_url:str = '/dashboard/reset/done'

def dashboard(request):
    shoots = Shoot.objects.filter(booked=True, complete=False)
    transactions = Transaction.objects.filter(complete=True, viewed=False)
    client_messages = Message.objects.filter(read=False)

    context = {
        "shoots": shoots,
        "transactions": transactions,
        "client_messages": client_messages,
    }

    return render(request, "dashboard.html", context)


def message_create(request):
    form = MessageForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Message sent successfully")
        return redirect("home")
    else:
        messages.error(request, "Message not sent. Please check your inputs.")
        return redirect("home")


class TransactionsList(ListView):
    model = Transaction
    template_name: str = "transactions.html"
    context_object_name: str = "transactions"
    paginate_by: int = 10


class MessagesList(ListView):
    model = Message
    template_name: str = "messages.html"
    context_object_name: str = "client_messages"
    paginate_by: int = 10


class ShootsList(ListView):
    model = Shoot
    template_name: str = "shoots.html"
    context_object_name: str = "shoots"
    paginate_by: int = 10


class ShootDetail(DetailView):
    model = Shoot
    template_name: str = "shoot.html"
    context_object_name: str = "shoot"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shoot = super().get_object()
        packages = shoot.package.all()
        context["packages"] = packages
        return context


class TransactionDetail(DetailView):
    model = Transaction
    template_name: str = "transaction.html"
    context_object_name: str = "transaction"


class ClientDetail(DetailView):
    model = Client
    template_name: str = "client.html"
    context_object_name: str = "client"


class ClientList(ListView):
    model = Client
    template_name: str = "clients.html"
    context_object_name: str = "clients"
    paginate_by: int = 15


class MessageDetail(DetailView):
    model = Message
    template_name: str = "message.html"
    context_object_name: str = "client_message"


@api_view(["GET", "POST"])
def set_shoot_complete(request):
    serializer = SetShootCompleteSerializer(data=request.data)
    if serializer.is_valid():
        print(serializer.validated_data)


@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def send_my_message(request):
    serializer = MyMessageSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        print(serializer.validated_data)
