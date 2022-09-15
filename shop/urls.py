from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('gallery', gallery, name='gallery'),
    path('gallery/upload', image_upload_view, name='image-upload'),
    path('packages', package , name='packages')
]