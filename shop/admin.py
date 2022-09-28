from django.contrib import admin

from shop.models import Client, GalleryImage, Package, Shoot

# Register your models here.
admin.site.register(GalleryImage)
admin.site.register(Package)
admin.site.register(Shoot)
admin.site.register(Client)