from http import client
from django.db import models


# Create your models here.
class Package(models.Model):
    nature_choice = [
        ('PHOTOGRAHY', 'PHOTOGRAHY'),
        ('VIDEOGRAPHY', 'VIDEOGRAPHY'),
    ]

    category_choices = [
        ('BRONZE', 'BRONZE'),
        ('SILVER', 'SILVER'),
        ('GOLD', 'GOLD') 
    ]

    type_choices = [
        ('WEDDING', 'WEDDING'),
        ('PORTRAIT', 'PORTRAIT'),
        ('RURACIO', 'RURACIO')
    ]

    type = models.CharField(max_length=10, choices=type_choices, default='WEDDING')
    category = models.CharField(max_length=10, choices=category_choices, null=True, blank=True)
    nature = models.CharField(max_length=15, choices=nature_choice, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self) -> str:
        return self.type + ' ' + self.nature + ' ' +  self.category
    
        
class GalleryImage(models.Model):
    filename = models.CharField(max_length=100)
    display = models.BooleanField(default=False)
    download_url = models.CharField(max_length=1000)

class Client(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    email = models.EmailField()

class Shoot(models.Model):
    package = models.ManyToManyField(Package)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    location = models.CharField(max_length=25)
    booked = models.BooleanField(default=False)
    





