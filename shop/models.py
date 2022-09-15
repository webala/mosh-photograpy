from django.db import models


# Create your models here.
class Wedding(models.Model):
    pass

class Ruracio(models.Model):
    pass

class Portrait(models.Model):
    pass

class WeddingCategories(models.Model):
    pass

    
        
class GalleryImage(models.Model):
    filename = models.CharField(max_length=100)
    display = models.BooleanField(default=False)
    download_url = models.CharField(max_length=1000)

class Shoot(models.Model):
    pass

class Client(models.Model):
    pass


