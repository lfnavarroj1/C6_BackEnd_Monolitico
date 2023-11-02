from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer, User,UserCreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
import jwt, datetime

# Create your views here.
class RegisterUser(APIView):
    def post(self,request):
        serializer=UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginUser(APIView):
    def post(self,request):
        username=request.data['username']
        password=request.data['password']
        user=User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed("User no found!")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")
        
        payload={
            "username":user.username,
            "exp":datetime.datetime.utcnow()+datetime.timedelta(hours=8),
            "iat":datetime.datetime.utcnow()
        }
        token=jwt.encode(payload,'secret',algorithm="HS256")
        response=Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data={'jwt':token}
        return response

class GetUser(APIView):
    def get(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        user=User.objects.get(username=payload['username'])
        serializar=UserSerializer(user)
        return Response(serializar.data)


class LogoutUser(APIView):
    def post(self,request):
        response=Response()
        response.delete_cookie('jwt')
        response.data={
            "mesagge":"Success"
        }
        return response