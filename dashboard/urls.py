from django.urls import path, include
from .views import *

urlpatterns = [
    path("register", register_user, name="register"),
    path('accounts/', include('django.contrib.auth.urls')),
    path("", dashboard, name="dashboard"),
    path("transactions", TransactionsList.as_view(), name="transactions-list"),
    path("messages", MessagesList.as_view(), name="messages-list"),
    path("message/<pk>", MessageDetail.as_view(), name="messages-detail"),
    path("message/create", message_create, name="messages-create"),
    path('message/reply', send_my_message, name='send-message'),
    path("shoots", ShootsList.as_view(), name="shoots-list"),
    path("shoot/<pk>", ShootDetail.as_view(), name="shoot-detail"),
    path("shoot/complete", set_shoot_complete, name="set-shoot-complete"),
    path("transaction/<pk>", TransactionDetail.as_view(), name="transaction-detail"),
    path("clients", ClientList.as_view(), name="client-list"),
]
