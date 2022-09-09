from this import d
from .models import Package, PackageCateagory
from django.shortcuts import render

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