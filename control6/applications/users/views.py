from .serializers import UserSerializer, User,UserCreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime

from rest_framework import status

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

        user = User.objects.filter(username = username).first()
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
        


