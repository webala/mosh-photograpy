from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('gallery', gallery, name='gallery'),
    path('gallery/upload', image_upload_view, name='image-upload'),
    path('packages', package , name='packages'),
    path('shoot/<int:shoot_id>', shoot, name='shoot'),
    path('shoot/book', book_shoot, name='book-shoot'),
    # path('book/portrait', book_portrait_shoot, name='book-portrait'),
    # path('book/ruracio', book_ruracio_shoot, name='book-ruracio'),
    path('shoot/pay/<int:shoot_id>', pay_shoot, name='pay-shoot'),
    path('stk_callback', mpesa_callback, name='mpesa-callback'),
    path('transaction/<request_id>', await_confirmation, name='await-confirmation'),
    path('receipt/<transaction_id>', download_receipt, name='download-receipt'),
]