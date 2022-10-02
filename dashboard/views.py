
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from shop.models import Message, Shoot, Transaction

# Create your views here.

def dashboard(request):
    shoots = Shoot.objects.filter(booked=True, complete=False)
    transactions = Transaction.objects.filter(complete=True, viewed=False)
    client_messages = Message.objects.filter(read=False)
    
    context = {
        'shoots': shoots,
        'transactions': transactions,
        'client_messages': client_messages
    }
    
    return render(request, 'dashboard.html', context)

class TransactionsList(ListView):
    model = Transaction
    template_name: str = 'transactions.html'
    context_object_name: str = 'transactions'
    paginate_by: int = 10

class MessagesList(ListView):
    model = Message
    template_name: str = 'messages.html'
    context_object_name: str = 'client_messages'
    paginate_by: int = 10

class ShootsList(ListView):
    model = Shoot
    template_name: str = 'shoots.html'
    context_object_name: str = 'shoots'
    paginate_by: int = 10

class ShootDetail(DetailView):
    model = Shoot
    template_name: str = 'shoot.html'
    context_object_name: str = 'shoot'