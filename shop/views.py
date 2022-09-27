from django.http import HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
import json, io
from shop.forms import ClientForm, ImageUploadForm, ShootForm
from shop.utils import get_image_url, initiate_stk_push, upload_image, auth, email, password
from .models import GalleryImage, Package, Shoot, Transaction
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib import messages
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas

# Create your views here.

def home(request):
    
   context = {}
   return render(request, 'home.html', context)


def gallery(request):
   photos = GalleryImage.objects.all()
   #query photos 10 at a time
   paginator = Paginator(photos, 10)
   page_number = request.GET.get('page') #get page number from GET request
   page_obj = paginator.get_page(page_number)
   
   context = {
      'page_obj': page_obj
   }

   return render(request, 'gallery.html', context)

def image_upload_view(request):
   form = ImageUploadForm(request.POST or None, request.FILES or None)

   context = {
      'form': form
   }

   if form.is_valid():
      
      data = form.cleaned_data
      image = data.get('image')
      
      
      #Upload image to firebase
      filename = upload_image('gallery', image)
      image = GalleryImage.objects.create(filename=filename)
      image_url = get_image_url('gallery', filename)
      image.download_url = image_url
      image.save()
      messages.success('Image uploaded successfully.')
      form = ImageUploadForm()
      context['form'] = form
      return render(request, 'image-upload.html', context)
   
   return render(request, 'image-upload.html', context)

def package(request):
   packages = Package.objects.all()

   context = {
      'packages': packages
   }
   
   return render(request, 'packages.html', context)

def book_wedding_shoot(request):
   client_form = ClientForm(request.POST or None)
   shoot_form = ShootForm(request.POST or None)

   contex = {
      'client_form': client_form,
      'shoot_form': shoot_form
   }

   if request.method == 'POST':
      if not request.POST.get('photography') and not request.POST.get('videography'):
         messages.error(request, 'Please select a package')
         return render(request, 'book_wedding.html', contex)

      if client_form.is_valid() and shoot_form.is_valid():
         client = client_form.save()
         shoot = shoot_form.save(commit=False)
         shoot.client = client
         shoot.save()

         if request.POST.get('photography'):
            category = request.POST.get('photography_category')
            print(category)
            package = Package.objects.filter(
               nature='PHOTOGRAHY',
               category=category,
               type='WEDDING'
            ).first()
            shoot.package.add(package)
            shoot.cost += int(package.price
)
         if request.POST.get('videography'):
            category = request.POST.get('videography_category')
            print(category)
            package = Package.objects.filter(
               nature='VIDEOGRAPHY',
               category=category,
               type='WEDDING'
            ).first()
            shoot.package.add(package)
            shoot.cost += int(package.price)
         
         shoot.save()
         
         messages.success(request, 'Shoot booked successfully.')
         return redirect('pay-shoot', shoot_id=shoot.id)

   return render(request, 'book_wedding.html', contex)

def book_portrait_shoot(request):
   client_form = ClientForm(request.POST or None)
   shoot_form = ShootForm(request.POST or None)

   contex = {
      'client_form': client_form,
      'shoot_form': shoot_form
   }

   if request.method == 'POST':
      if not request.POST.get('portrait_category'):
         messages.error(request, 'Please select a package')
         return render(request, 'book_portrait.html', contex)

      if client_form.is_valid() and shoot_form.is_valid():
         client = client_form.save()
         shoot = shoot_form.save(commit=False)
         shoot.client = client
         shoot.save()

         category = request.POST.get('portrait_category')
         package = Package.objects.filter(
            category=category,
            type='PORTRAIT',
            nature='PHOTOGRAHY'
         ).first()

         shoot.package.add(package)
         shoot.cost += int(package.price)
         shoot.save()

         messages.success(request, 'Shoot booked successfully.')
         return redirect('pay-shoot', shoot_id=shoot.id)
   return render(request, 'book_portrait.html', contex)

def book_ruracio_shoot(request):
   client_form = ClientForm(request.POST or None)
   shoot_form = ShootForm(request.POST or None)

   contex = {
      'client_form': client_form,
      'shoot_form': shoot_form
   }

   if request.method == 'POST':
      if not request.POST.get('photography') and not request.POST.get('videography'):
         messages.error(request, 'Please select a package')
         return render(request, 'book_ruracio.html', contex)

      if client_form.is_valid() and shoot_form.is_valid():
         client = client_form.save()
         shoot = shoot_form.save(commit=False)
         shoot.client = client
         shoot.save()

         if request.POST.get('photography'):
            nature = request.POST.get('photography')
            package = Package.objects.filter(
               nature=nature,
               type='RURACIO'
            ).first()

            shoot.package.add(package)
            shoot.cost += int(package.price)

         if request.POST.get('videography'):
            nature = request.POST.get('videography')
            package = Package.objects.filter(
               nature=nature,
               type='RURACIO'
            ).first()

            shoot.package.add(package)
            shoot.cost += int(package.price)
         
         shoot.save()

         messages.success(request, 'Shoot booked successfully.')
         return redirect('pay-shoot', shoot_id=shoot.id)

   return render(request, 'book_ruracio.html', contex)


def pay_shoot(request, shoot_id):
   shoot = Shoot.objects.get(id=shoot_id)
   packages = shoot.package.all()
   context = {
    'shoot': shoot,
    'packages': packages  
   }

   if request.method == 'POST':
      phone = request.POST.get('phone')
      deposit_amount = 1000
      transaction_data = initiate_stk_push(phone, deposit_amount)
      request_id = transaction_data.get('chechout_request_id')
      transaction = Transaction.objects.create(
         shoot=shoot,
         request_id=request_id,
      )
      return redirect('await-confirmation', request_id=request_id)
   return render(request, 'pay_shoot.html', context)


def await_confirmation(request, request_id):
   transaction = Transaction.objects.get(request_id=request_id)
   context = {
     'transaction': transaction 
   }
   return render(request, 'await_confirmation.html', context)

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

            return HttpResponse('Ok')

def download_receipt(request, transaction_id):
   transaction = Transaction.objects.get(id=transaction_id)
   buffer = io.BytesIO()
   p = canvas.Canvas(buffer)

   p.drawString(0, 720, 'GLITCH CLOUD PHOTOGRAPHY')
   p.drawString(10, 690, 'Payment for shoot')
   p.drawString(10, 675, 'Receipt No: {}'.format(transaction.receipt_number))
   p.drawString(10, 660, 'Date: {}'.format(transaction.date))
   p.drawString(10, 645, 'Client: {} {}'.format(transaction.shoot.client.first_name, transaction.shoot.client.last_name))
   p.drawString(10, 630, 'Phone {}'.format(transaction.phone_number))
   p.drawString(10, 615, 'Thank you for doing business with us.')
   p.showPage()
   p.save()

   buffer.seek(0)
   return FileResponse(buffer, as_attachment=True, filename='Receipt.pdf')
   