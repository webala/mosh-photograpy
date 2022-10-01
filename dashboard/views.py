
from django.shortcuts import render

from shop.models import Message, Shoot, Transaction

# Create your views here.

def dashboard(request):
    shoots = Shoot.objects.all()[:7]
    transactions = Transaction.objects.all()[:7]
    messages = Message.objects.all()[:7]
    
    context = {
        'shoots': shoots,
        'transactions': transactions,
        'messages': messages
    }
    
    return render(request, 'dashboard.html', context)