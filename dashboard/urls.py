from django.urls import path
from .views import *

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("transactions", TransactionsList.as_view(), name="transactions-list"),
    path("messages", MessagesList.as_view(), name="messages-list"),
    path("shoots", ShootsList.as_view(), name="shoots-list"),
    path("shoot/<pk>", ShootDetail.as_view(), name="shoot-detail"),
]
