from django.db import models

# Create your models here.
class Package(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name + ' ' + self.type

class PackageCateagory(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category_description = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.package.name + ' ' + self.package.type + ' ' + self.name


class Shoot(models.Model):
    pass

class Client(models.Model):
    pass

