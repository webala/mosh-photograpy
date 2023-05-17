from django.contrib import admin

from shop.models import Client, GalleryImage, Package, Shoot, ServiceCategory, Service, Transaction, BookedService

# Register your models here.
admin.site.register(GalleryImage)
admin.site.register(Package)
admin.site.register(Shoot)
admin.site.register(Client)
admin.site.register(Service)
admin.site.register(ServiceCategory)
admin.site.register(Transaction)
admin.site.register(BookedService)