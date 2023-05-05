from rest_framework import serializers
from .models import Client, Shoot, GalleryImage, Service, ServiceCategory, BookedService, Transaction

class ClientSerializer(serializers.ModelSerializer):
     class Meta:
          model = Client
          fields = "__all__"

class PackgesSerializer(serializers.Serializer):
     nature = serializers.CharField()
     category = serializers.CharField(required=False)
     type = serializers.CharField()



class PhoneNumberSerializer(serializers.Serializer):
     phoneNumber = serializers.CharField()

class GallerySerializer(serializers.ModelSerializer):
     class Meta:
          model = GalleryImage
          fields = "__all__"

class UploadImageSerializer(serializers.Serializer):
    image = serializers.ImageField()

class CategorySerializer(serializers.ModelSerializer):
     id = serializers.IntegerField()
     class Meta:
          model = ServiceCategory
          fields = "__all__"

class ServiceSerializer(serializers.ModelSerializer):
     category = CategorySerializer(many=True)
     class Meta:
          model = Service
          fields = "__all__"

     
     def create(self, validated_data):
          service = Service.objects.create(
               name = validated_data.get('name'),
               description=validated_data.get('description'),
               price = validated_data.get('price'),
               quantifiable = validated_data.get('quantifiable')
          )
          categories = validated_data.get('category')
          for value in categories:
               print('value: ', value)
               category = ServiceCategory.objects.get(
                    id=value.get('id')
               )
               service.category.add(category)
          
          return service



class BookedServiceSerializer(serializers.ModelSerializer):
     service = ServiceSerializer()
     class Meta:
          model = BookedService
          fields = "__all__"

class ShootSerializer(serializers.ModelSerializer):
     id = serializers.IntegerField()
     booked_services = BookedServiceSerializer(many=True)
     client = ClientSerializer(required=False)
     class Meta:
          model = Shoot
          fields = ['id','client', 'date', 'location', 'description', 'booked', 'cost', 'complete', 'booked_services']
     
     def create(self, validated_data):
          shoot = Shoot.objects.create(
               date=validated_data.get('date'),
               location=validated_data.get('location'),
               description=validated_data.get('description')
          )

          booked_services = validated_data.get('booked_services')
          for value in booked_services:
               service_values = value.get('service')
               service_query = Service.objects.filter(
                    name=service_values.get('name'),
                    description=service_values.get('description'),
                    price=service_values.get('price'),
                    quantifiable=service_values.get('quantifiable')
               )
               service = service_query.first()
               booked_service, created = BookedService.objects.get_or_create(
                    service = service,
                    quantity = value.get('quantity')
               )
               print('book service: ', booked_services)
               shoot.booked_services.add(booked_service)
               print('added')
               
          return shoot



class PaymentSerializer(serializers.Serializer):
     shoot = ShootSerializer()