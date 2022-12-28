from builtins import print
from django.http import HttpResponse, FileResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import json, io
from shop.forms import ClientForm, ImageUploadForm, MessageForm, ShootForm
from shop.utils import (
    get_image_url,
    initiate_stk_push,
    upload_image,
    auth,
    email,
    password,
)
from .models import GalleryImage, Package, Shoot, Transaction, Client
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib import messages
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from dashboard.serializers import SetShootCompleteSerializer
from .serializers import BookShootSerializer, ClientSerializer, PackgesSerializer, ShootSerializer

# Create your views here.


def home(request):
    message_form = MessageForm()

    context = {"message_form": message_form}

    return render(request, "home.html", context)


def gallery(request):
    photos = GalleryImage.objects.filter(display=True)
    # query photos 10 at a time
    paginator = Paginator(photos, 10)
    page_number = request.GET.get("page")  # get page number from GET request
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj}

    return render(request, "gallery.html", context)


def image_upload_view(request):
    form = ImageUploadForm(request.POST or None, request.FILES or None)

    context = {"form": form}

    if form.is_valid():

        data = form.cleaned_data
        image = data.get("image")

        # Upload image to firebase
        filename = upload_image("gallery", image)
        image = GalleryImage.objects.create(filename=filename)
        user = auth.sign_in_with_email_and_password(email, password)
        image_url = get_image_url("gallery", filename, user)
        image.download_url = image_url
        image.save()
        messages.success(request, "Image uploaded successfully.")
        form = ImageUploadForm()
        context["form"] = form
        return render(request, "image-upload.html", context)

    return render(request, "image-upload.html", context)


def package(request):
    packages = Package.objects.all()
    client_form = ClientForm()
    shoot_form = ShootForm()

    context = {
        "packages": packages,
        "client_form": client_form,
        "shoot_form": shoot_form,
    }

    return render(request, "packages.html", context)


@api_view(['POST'])
@permission_classes([AllowAny])
def book_shoot(request):
    shoot_serializer = BookShootSerializer(data = request.data)
    

    if shoot_serializer.is_valid(raise_exception=True):
        print('data; ', shoot_serializer.validated_data)
        data = shoot_serializer.validated_data
        client_data = data.get('client')
        client = Client.objects.create(
            first_name=client_data.get('first_name'),
            last_name=client_data.get('last_name'),
            phone=client_data.get('phone'),
            email=client_data.get('email')
        )

        print('client: ', client)
        shoot_data = data.get('shoot')

        shoot = Shoot.objects.create(
            client=client,
            date=shoot_data.get('date'),
            location=shoot_data.get('location'),
        )

        print('shoot: ', shoot)
        cost = 0
        packages = data.get('packages')

        for item in packages:
            if item.get('category'):
                print('item with category: ', item)

                print('type: ', item.get('type'))
                pkg = Package.objects.filter(
                    category=item.get('category'),
                    nature=item.get('nature'),
                    type=item.get('type')
                )

                print('pkg ', pkg)

                if pkg.exists():
                    pkg = pkg.first()
                    cost += pkg.price
                    shoot.package.add(pkg)
                else:
                    return Response({'Message': "Invalid Package"}, 404)
            else:
                print('item no category: ', item)
                pkg = Package.objects.filter(
                    nature=item.get('nature'),
                    type=item.get('type')
                )

                if pkg.exists():
                    pkg = pkg.first()
                    cost += pkg.price
                    shoot.package.add(pkg)
                else:
                    return Response({'Message': "Invalid Package"}, 404)
        shoot.cost = cost
        shoot.save()

        
        return Response({'message': 'shoot booked', "id": shoot.id}, 201)
    return Response({"Message": "Bad request"}, 400)
    


def pay_shoot(request, shoot_id):
    shoot = Shoot.objects.get(id=shoot_id)
    packages = shoot.package.all()
    context = {"shoot": shoot, "packages": packages}

    if request.method == "POST":
        phone = request.POST.get("phone")
        deposit_amount = 1000
        transaction_data = initiate_stk_push(phone, deposit_amount)
        request_id = transaction_data.get("chechout_request_id")
        transaction = Transaction.objects.create(
            shoot=shoot,
            request_id=request_id,
        )
        return redirect("await-confirmation", request_id=request_id)
    return render(request, "pay_shoot.html", context)


def await_confirmation(request, request_id):
    transaction = Transaction.objects.get(request_id=request_id)

    context = {"transaction": transaction}# class PasswordResetConfirm(PasswordResetConfirmView):
#     success_url:str = '/dashboard/reset/done'
    return render(request, "await_confirmation.html", context)


@csrf_exempt
def mpesa_callback(request):
    if request.method == "POST":
        request_data = json.loads(request.body)
        body = request_data.get("Body")
        result_code = body.get("stkCallback").get("ResultCode")

        if result_code == 0:
            print("Payment successful")
            request_id = body.get("stkCallback").get("CheckoutRequestID")
            metadata = body.get("stkCallback").get("CallbackMetadata").get("Item")

            for data in metadata:
                if data.get("Name") == "MpesaReceiptNumber":
                    receipt_number = data.get("Value")
                elif data.get("Name") == "Amount":
                    amount = data.get("Value")
                elif data.get("Name") == "PhoneNumber":
                    phone_number = data.get("Value")
            print("receipt:", receipt_number)
            print("amouont: ", amount)
            print("request_id: ", request_id)
            transaction = Transaction.objects.get(request_id=request_id)
            transaction.receipt_number = receipt_number
            transaction.amount = amount
            transaction.phone_number = str(phone_number)
            transaction.complete = True
            transaction.save()

            shoot = transaction.shoot
            shoot.booked = True
            shoot.save()

            return HttpResponse("Ok")


def download_receipt(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    p.drawString(0, 720, "GLITCH CLOUD PHOTOGRAPHY")
    p.drawString(10, 690, "Payment for shoot")
    p.drawString(10, 675, "Receipt No: {}".format(transaction.receipt_number))
    p.drawString(10, 660, "Date: {}".format(transaction.date))
    p.drawString(
        10,
        645,
        "Client: {} {}".format(
            transaction.shoot.client.first_name, transaction.shoot.client.last_name
        ),
    )
    p.drawString(10, 630, "Phone {}".format(transaction.phone_number))
    p.drawString(10, 615, "Thank you for doing business with us.")
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="Receipt.pdf")
