from shop.forms import ImageUploadForm
from shop.utils import upload_image
from .models import GalleryImage, Package, PackageCateagory
from django.shortcuts import render
from django.views.generic import CreateView

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
   return render(request, 'gallery.html')

def image_upload_view(request):
   form = ImageUploadForm(request.POST or None)

   context = {
      'form': form
   }

   if form.is_valid():
      filename = upload_image()
      GalleryImage.objects.create(filename=filename)
      form = ImageUploadForm()
      context['form'] = form
      return render(request, 'image-upload.html', context)
   
   return render(request, 'image-upload.html', context)