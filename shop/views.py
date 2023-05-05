
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
    initiate_pesapal_transaction,
    get_transaction_status
)
from .models import GalleryImage, Package, Shoot, Transaction, Client, Service, ServiceCategory
from django.shortcuts import render
from django.contrib import messages
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import ShootSerializer, PhoneNumberSerializer, GallerySerializer, UploadImageSerializer, ServiceSerializer, CategorySerializer, PaymentSerializer
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

class CategoriesListCreateView(generics.ListCreateAPIView):
    queryset = ServiceCategory.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny, )

class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = (AllowAny, )

class ServiceView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = (AllowAny, )

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

class GalleryView(generics.ListAPIView):
    queryset = GalleryImage.objects.all()
    serializer_class = GallerySerializer
    permission_classes = (AllowAny, )

@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([FormParser, MultiPartParser])
def image_upload_view(request):
    serializer = UploadImageSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data

        image = data.get('image')
        filename = upload_image('gallery', image)
        user = auth.sign_in_with_email_and_password(email, password)
        image_url = get_image_url('gallery', filename, user)
        gallery_image = GalleryImage.objects.create(
            filename=filename,
            download_url=image_url
        )

        serializer = GallerySerializer(gallery_image)

        return Response(serializer.data, status=200)
   


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


class ShootView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shoot.objects.all()
    serializer_class = ShootSerializer
    permission_classes = [AllowAny]

class ShootListCreateView(generics.ListCreateAPIView):
    serializer_class = ShootSerializer
    queryset = Shoot.objects.all()
    permission_classes = [AllowAny]
    



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


class ProcessPayment(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            shood_data = data.get('shoot')
            print('shoot: ', shood_data.get('id'))
            shoot = Shoot.objects.get(id=shood_data.get('id'))
            description = "Payment for shoot #{}".format(shoot.id)
            transaction = Transaction.objects.create(
                shoot=shoot
            )
            response = initiate_pesapal_transaction(description, transaction.id)
            order_tracking_id = response.get('order_tracking_id')
            transaction.order_tracking_id = order_tracking_id
            transaction.save()

            return Response(response, status=200)

@csrf_exempt
def pesapal_ipn(request):
    data = json.loads(request.body)
    order_tracking_id = data.get('OrderTrackingId')
    transaction_query = Transaction.objects.filter(order_tracking_id=order_tracking_id)
    if transaction_query.exists():
        transaction = transaction_query.first()
        transaction_status = get_transaction_status(order_tracking_id)
        print('transaction status: ', transaction_status)
        transaction.payment_method = transaction_status.get('payment_method')
        transaction.amount = transaction_status.get('amount')
        transaction.confirmation_code = transaction_status.get('confirmation_code')
        transaction.payment_status = transaction_status.get('payment_status_description')
        transaction.payment_status_description = transaction_status.get('description')
        transaction.payment_currency = transaction_status.get('currency')
        transaction.save()
        shoot = transaction.shoot
        if transaction.payment_status.lower() == 'completed':
            shoot.booked = True
            shoot.save()
        return HttpResponse('OK')
    
