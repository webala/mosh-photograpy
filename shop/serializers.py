from rest_framework import serializers
from .models import Client, Shoot, GalleryImage, Service, ServiceCategory

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

class ShootSerializer(serializers.ModelSerializer):
     services = ServiceSerializer(many=True)
     client = ClientSerializer(required=False)
     class Meta:
          model = Shoot
          fields = ['client', 'date', 'location', 'description', 'booked', 'cost', 'complete', 'services']
     
     def create(self, validated_data):
          shoot = Shoot.objects.create(
               date=validated_data.get('date'),
               location=validated_data.get('location'),
               description=validated_data.get('description')
          )

          services = validated_data.get('services')
          for value in services:
               service = Service.objects.get(
                    name=value.get('name'),
                    description=value.get('description'),
                    price=value.get('price')
               )
               shoot.services.add(service)
          
          return shoot



class BookShootSerializer(serializers.Serializer):
     shoot = ShootSerializer()
     client = ClientSerializer()
     packages= PackgesSerializer(many=True)