
from django.shortcuts import render

from shop.models import Shoot, Transaction

# Create your views here.

def dashboard(request):
    shoots = Shoot.objects.all()[:7]
    transactions = Transaction.objects.all()[:7]
    
    return render(request, 'dashboard.html')