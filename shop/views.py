from shop.forms import ImageUploadForm
from shop.utils import get_image_url, upload_image, auth, email, password
from .models import GalleryImage, Package, PackageCateagory
from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.

def home(request):
    package_categories = PackageCateagory.objects.all()
    packages = Package.objects.all()

    context = {
       'packages': packages,
       'package_categories': package_categories
    }

    return render(request, 'home.html', context)


def gallery(request):
   photos = GalleryImage.objects.all()

   #query photos 10 at a time
   paginator = Paginator(photos, 10)
   page_number = request.GET.get('page') #get page number from GET request
   page_obj = paginator.get_page(page_number)
   

   user = auth.sign_in_with_email_and_password(email, password)
   download_urls = []
   # for obj in page_obj:
   #    #Get download urls from firebase
   #    url = get_image_url('gallery', obj.filename, user)
   #    download_urls.append(url)
   
   
   context = {
      'download_urls': download_urls,
      'page_obj': page_obj
   }

   return render(request, 'gallery.html', context)

def image_upload_view(request):
   form = ImageUploadForm(request.POST or None, request.FILES or None)

   context = {
      'form': form
   }

   if form.is_valid():
      
      data = form.cleaned_data
      image = data.get('image')
      
      
      #Upload image to firebase
      filename = upload_image('gallery', image)
      image = GalleryImage.objects.create(filename=filename)
      image_url = get_image_url('gallery', filename)
      image.download_url = image_url
      image.save()
      
      form = ImageUploadForm()
      context['form'] = form
      return render(request, 'image-upload.html', context)
   
   return render(request, 'image-upload.html', context)