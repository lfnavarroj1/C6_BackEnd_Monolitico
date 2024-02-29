from .serializers import UserSerializer, User,UserCreateSerializer,ChangePasswordSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from django.contrib.auth.views import PasswordChangeView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import SetPasswordForm
from ..static_data.models.contrato import Contrato


class RegisterUser(APIView):
    def post(self, request):
        user = ValidateUser(request)
        serializer = UserCreateSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginUser(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        

        user = User.objects.filter(username=username).first()

        print(user)
        if user is None:
            raise AuthenticationFailed("Usuario no encontrado")
        if not user.check_password(password):
            raise AuthenticationFailed("Contraseña incorrecta")

        payload = {
            "username": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours = 8),
            "iat": datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm = "HS256")
        response = Response()

        response.set_cookie(key = 'jwt', value = token, httponly = True)
        response.data = {'jwt': token}

        return response

class GetUser(APIView):
    def get(self, request):
        user = ValidateUser (request)
        serializar = UserSerializer(user)
        return Response(serializar.data)


class LogoutUser(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "mesagge":"Success"
        }
        return response    

class UpdateUser(APIView):
    def put(sefl, request):
        return Response({'message': 'Usuario actualizado correctamente'}, status=status.HTTP_200_OK)


class DeleteUser(APIView):
    def delete():
        pass

class ChangePasswordUser(APIView):
    def post(self, request):
        user = ValidateUser(request)

        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")

            if not user.check_password(old_password):
                return Response({"old_password": ["Contraseña actual incorrecta."]}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({"message": "Contraseña cambiada exitosamente."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def ValidateUser(request):       
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Usuario no autenticado")
        
        try:
            payload = jwt.decode(token,'secret', algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Usuario no autenticado")
        user = User.objects.get(username=payload['username'])
        return user
        


