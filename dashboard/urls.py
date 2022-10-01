from django.urls import path
from .views import *

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('transactions', TransactionsList.as_view(), name='transactions-list'),
    path('messages', MessagesList.as_view(), name='messages-list')
]