from shop.forms import ClientForm, ImageUploadForm, ShootForm
from shop.utils import get_image_url, upload_image, auth, email, password
from .models import GalleryImage, Package
from django.shortcuts import render
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
   client_form = ClientForm()
   shoot_form = ShootForm()

   contex = {
      'client_form': client_form,
      'shoot_form': shoot_form
   }

   return render(request, 'book_wedding.html', contex)