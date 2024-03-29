from email import message
from email.policy import default
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
        if self.type == 'RURACIO':
            return self.type + ' ' + self.nature
        else:
            return self.type + ' ' + self.nature + ' ' +  self.category
    
        
class GalleryImage(models.Model):
    filename = models.CharField(max_length=100)
    display = models.BooleanField(default=False)
    download_url = models.CharField(max_length=1000)

    class Meta:
        ordering = ['-id']

class ServiceCategory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    category = models.ManyToManyField(ServiceCategory)
    quantifiable = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']

class BookedService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)

    @property
    def price(self):
        return self.service.price * self.quantity

class Client(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    email = models.EmailField()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Shoot(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    location = models.CharField(max_length=25)
    description = models.CharField(max_length=300)
    booked = models.BooleanField(default=False)
    cost = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    complete = models.BooleanField(default=False)
    booked_services = models.ManyToManyField(BookedService)

    def __str__(self):
        return self.location + ' ' + str(self.date)

    @property
    def total(self):
        return sum([(booked_service.service.price * booked_service.quantity) for booked_service in self.booked_services])

class Transaction(models.Model):
    order_tracking_id = models.CharField(max_length=50, null=True)
    shoot = models.ForeignKey(Shoot, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=30, null=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    confirmation_code = models.CharField(max_length=30, null=True)
    payment_status = models.CharField(max_length=20, null=True)
    payment_status_description = models.CharField(max_length=50, null=True)
    payment_currency = models.CharField(max_length=5, null=True)

class Message(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=20)
    message = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)


class MyMessage(models.Model):
    replied_message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)
    




