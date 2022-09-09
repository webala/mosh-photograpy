from this import d
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

class GalleryImageCreate(CreateView):
   model = GalleryImage
   template_name: str = 'image-upload.html'
   