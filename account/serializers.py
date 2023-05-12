from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
         }
        
    def validate(self, attrs):
      if attrs['password1'] != attrs['password2']:
         raise serializers.ValidationError({'password', 'Password fields do not match'})
      
      return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
        )

        print('password: ', validated_data.get('password1'))

        user.set_password(validated_data.get('password1'))
        user.save()
        return user

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