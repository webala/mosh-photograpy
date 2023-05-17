from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('gallery', GalleryView.as_view(), name='gallery'),
    path('gallery/upload', image_upload_view, name='image-upload'),
    path('packages', package , name='packages'),
    path('services', ServiceListCreateView.as_view() , name='services'),
    path('categories', CategoriesListCreateView.as_view() , name='categories'),
    path('service/<pk>', ServiceView.as_view() , name='service'),
    path('shoot/<int:pk>', ShootView.as_view(), name='shoot'),
    path('image/<int:pk>', ImageDetail.as_view(), name='image'),
    path('image/delete/<int:image_id>', delete_image_view, name='delete-image'),
    path('shoots', ShootListCreateView.as_view(), name='book-shoot'),
    path('stk_callback', mpesa_callback, name='mpesa-callback'),
    path('transaction/<request_id>', await_confirmation, name='await-confirmation'),
    path('receipt/<transaction_id>', download_receipt, name='download-receipt'),
    path('payment', ProcessPayment.as_view(), name='process-payment'),
    path('payment/ipn', pesapal_ipn, name='payment-notification'),
]