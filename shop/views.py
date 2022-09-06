from .models import PackageCateagory
from django.shortcuts import render

# Create your views here.

def home(request):
    packages = PackageCateagory.objects.all()

    context = {
       'packages': packages 
    }
    
    return render(request, 'home.html', context)
