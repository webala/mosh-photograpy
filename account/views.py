from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer, MyTokenObtainPairSerializer,LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate

# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class MyTokenObtainView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

class Logout(APIView):
    permission_classes = (IsAuthenticated, )
    def post(self, request):
        # try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=200)
        # except Exception as e:
        #     return Response(status=400)

class UsersList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # pagination_class = ResultPagination

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Login(APIView):
     permission_classes = [AllowAny]
     def post(self, request):
          serialiser = LoginSerializer(data=request.data)
          if serialiser.is_valid(raise_exception=True):
               username = serialiser.validated_data.get('username')
               password = serialiser.validated_data.get('password')
               user = authenticate(username=username, password=password)
               if user is not None:
                    serialiser = UserSerializer(user)
                    return Response(serialiser.data, status=200)
               else:
                    return Response({'message': 'Invalid username or password'}, 401)
          return Response({'message': 'Bad request'}, status=400)

