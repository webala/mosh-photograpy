from rest_framework import serializers
from .models import Client, Shoot, GalleryImage, Service, ServiceCategory, BookedService

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
     class Meta:
          model = ServiceCategory
          fields = "__all__"

class ServiceSerializer(serializers.ModelSerializer):
     category = CategorySerializer(many=True)
     class Meta:
          model = Service
          fields = "__all__"

class BookedServiceSerializer(serializers.ModelSerializer):
     service = ServiceSerializer()
     class Meta:
          model = BookedService
          fields = "__all__"

class ShootSerializer(serializers.ModelSerializer):
     booked_services = BookedServiceSerializer(many=True)
     client = ClientSerializer(required=False)
     class Meta:
          model = Shoot
          fields = ['client', 'date', 'location', 'description', 'booked', 'cost', 'complete', 'booked_services']
     
     def create(self, validated_data):
          shoot = Shoot.objects.create(
               date=validated_data.get('date'),
               location=validated_data.get('location'),
               description=validated_data.get('description')
          )

          booked_services = validated_data.get('booked_services')
          for value in booked_services:
               service_values = value.get('service')
               service = Service.objects.get(
                    name=service_values.get('name'),
                    description=service_values.get('description'),
                    price=service_values.get('price'),
                    quantifiable=service_values.get('quantifiable')
               )
               booked_service, created = BookedService.objects.get_or_create(
                    service = service,
                    quantity = value.get('quantity')
               )
               print('book service: ', booked_services)
               shoot.booked_services.add(booked_service)
               print('added')
               
          return shoot



class BookShootSerializer(serializers.Serializer):
     shoot = ShootSerializer()
     client = ClientSerializer()
     packages= PackgesSerializer(many=True)