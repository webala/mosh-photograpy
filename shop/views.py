from shop.forms import ImageUploadForm
from shop.utils import get_image_url, upload_image
from .models import GalleryImage, Package, PackageCateagory
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib import messages

# Create your views here.

def home(request):
    package_categories = PackageCateagory.objects.all()
    packages = Package.objects.all()

    context = {
       'packages': packages,
       'package_categories': package_categories
    }

    return render(request, 'home.html', context)


def gallery(request):
   photos = GalleryImage.objects.all()

   context = {
      'photos': photos
   }

   return render(request, 'gallery.html', context)

def image_upload_view(request):
   form = ImageUploadForm(request.POST or None, request.FILES or None)

   context = {
      'form': form
   }

   if form.is_valid():
      print('form is valid')
      data = form.cleaned_data
      image = data.get('image')
      print('image: ', image)
      filename = upload_image('gallery', image)
      GalleryImage.objects.create(filename=filename)
      image_url = get_image_url('gallery', filename)
      print('image url: ', image_url)
      form = ImageUploadForm()
      context['form'] = form
      return render(request, 'image-upload.html', context)
   
   return render(request, 'image-upload.html', context)