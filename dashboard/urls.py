from re import template
from django.urls import path, include, reverse
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("register", register_user, name="register"),
    path(
        "password_reset",
        password_reset_request,
        name="password-reset",
    ),
    path(
        "password_reset_done",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_sent.html"
        ),
        name="password-reset-done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm_template.html",
            success_url='/dashboard/reset/done'
        ),
        name="password-reset-confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_confirm_done_template.html"
        ),
        name="password-reset-confirm-done",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", dashboard, name="dashboard"),
    path("transactions", TransactionsList.as_view(), name="transactions-list"),
    path("messages", MessagesList.as_view(), name="messages-list"),
    path("message/<int:pk>", MessageDetail.as_view(), name="message-detail"),
    path("message/create", message_create, name="messages-create"),
    path("message/reply", send_my_message, name="send-message"),
    path("shoots", ShootsList.as_view(), name="shoots-list"),
    path("shoot/<int:pk>", ShootDetail.as_view(), name="shoot-detail"),
    path("shoot/complete", set_shoot_complete, name="set-shoot-complete"),
    path("transaction/<pk>", TransactionDetail.as_view(), name="transaction-detail"),
    path("clients", ClientList.as_view(), name="client-list"),
    path("client/<int:pk>", ClientDetail.as_view(), name="client-detail"),
]
