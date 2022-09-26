from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('gallery', gallery, name='gallery'),
    path('gallery/upload', image_upload_view, name='image-upload'),
    path('packages', package , name='packages'),
    path('book/wedding', book_wedding_shoot, name='book-wedding'),
    path('shoot/pay/<int:shoot_id>', pay_shoot, name='pay-shoot'),
    path('stk_callback', mpesa_callback, name='mpesa-callback'),
    path('transaction/<request_id>', await_confirmation, name='await-confirmation'),
    path('receipt/<transaction_id>', download_receipt, name='download-receipt')
]