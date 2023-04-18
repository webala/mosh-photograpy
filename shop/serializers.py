from rest_framework import serializers
from .models import Client, Shoot, GalleryImage, Service

class ClientSerializer(serializers.ModelSerializer):
     class Meta:
          model = Client
          fields = [
               'first_name',
               'last_name',
               'phone',
               'email'
          ]

class PackgesSerializer(serializers.Serializer):
     nature = serializers.CharField()
     category = serializers.CharField(required=False)
     type = serializers.CharField()

class ShootSerializer(serializers.ModelSerializer):
     class Meta:
          model = Shoot
          fields = [
               'date',
               'location',
          ]

class BookShootSerializer(serializers.Serializer):
     shoot = ShootSerializer()
     client = ClientSerializer()
     packages= PackgesSerializer(many=True)

class PhoneNumberSerializer(serializers.Serializer):
     phoneNumber = serializers.CharField()

class GallerySerializer(serializers.ModelSerializer):
     class Meta:
          model = GalleryImage
          fields = "__all__"

class UploadImageSerializer(serializers.Serializer):
    image = serializers.ImageField()

class ServiceSerializer(serializers.ModelSerializer):
     class Meta:
          model = Service
          fields = "__all__"