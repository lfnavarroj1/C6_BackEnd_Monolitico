from .serializers import UserSerializer, User,UserCreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt, datetime
from rest_framework import status


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
            return Response({"message": "Usuario no encontrado","valid_user":False}, status=status.HTTP_200_OK)
        if not user.check_password(password):
            return Response({"message": "Contraseña incorrecta","valid_user":False}, status=status.HTTP_200_OK)

        payload = {
            "username": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours = 8),
            "iat": datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm = "HS256")
        response = Response()

        response.set_cookie(key = 'jwt', value = token, httponly = True)
        response.data = {'jwt': token, "valid_user":True }

        return response

class GetUser(APIView):
    def get(self, request):
        response = ValidateUser (request)
        if response is None:
            return Response({"message": "Usuario no autenticado","valid_user":False}, status=status.HTTP_200_OK)

        data = UserSerializer(response)
        return Response({"user": data.data,"valid_user":True}, status=status.HTTP_200_OK)

class LogoutUser(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "mesagge":"Sesión cerrada"
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
            return None
        try:
            payload = jwt.decode(token,'secret', algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            return None
        response = User.objects.get(username=payload['username'])
        return response
        


