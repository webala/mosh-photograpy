from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        #Add custom claims
        
        token['username'] = user.username
        token['email'] = user.email
      #   token['groups'] = [group.name for group in list(user.groups.all())]
        token['id'] = user.id

        return token
   
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()