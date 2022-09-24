from shop.forms import ClientForm, ImageUploadForm, ShootForm
from shop.utils import get_image_url, upload_image, auth, email, password
from .models import GalleryImage, Package, Shoot
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib import messages
from django.core.paginator import Paginator

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
            if category == 'BRONZE':
               shoot.cost += 25000
            elif category == 'SILVER':
               shoot.cost += 33000
            elif category == 'GOLD':
               shoot.cost += 51000

         if request.POST.get('videography'):
            category = request.POST.get('videography_category')
            print(category)
            package = Package.objects.filter(
               nature='VIDEOGRAPHY',
               category=category,
               type='WEDDING'
            ).first()
            shoot.package.add(package)
            if category == 'BRONZE':
               shoot.cost += 20000
            elif category == 'SILVER':
               shoot.cost += 30000
            elif category == 'GOLD':
               shoot.cost += 50000
         
         shoot.save()
         
         messages.success(request, 'Shoot booked successfully.')
         return redirect('pay-shoot', shoot_id=shoot.id)

   return render(request, 'book_wedding.html', contex)

def pay_shoot(request, shoot_id):
   shoot = Shoot.objects.get(id=shoot_id)
   packages = shoot.package.all()
   context = {
    'shoot': shoot,
    'packages': packages  
   }
   return render(request, 'pay_shoot.html', context)