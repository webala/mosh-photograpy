from django.contrib import admin

from shop.models import Package, PackageCateagory

# Register your models here.
admin.site.register(Package)
admin.site.register(PackageCateagory)