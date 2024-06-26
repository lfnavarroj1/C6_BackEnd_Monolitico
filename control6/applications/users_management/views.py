# from .serializers import UserSerializer, User, UserCreateSerializer, ChangePasswordSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response
# import jwt, datetime
# from rest_framework import status
# from django.db.models import Q


# class RegisterUser(APIView):
#     def post(self, request):
#         user = ValidateUser(request)
#         serializer = UserCreateSerializer(data = request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
    

# class LoginUser(APIView):
#     def post(self, request):
#         username = request.data['username']
#         password = request.data['password']
#         user = User.objects.filter(username=username).first()

#         if user is None:
#             return Response({"message": "Usuario no encontrado","valid_user":False}, status=status.HTTP_200_OK)
#         if not user.check_password(password):
#             return Response({"message": "Contraseña incorrecta","valid_user":False}, status=status.HTTP_200_OK)

#         payload = {
#             "username": user.username,
#             "exp": datetime.datetime.utcnow() + datetime.timedelta(hours = 8),
#             "iat": datetime.datetime.utcnow()
#         }
#         token = jwt.encode(payload, 'secret', algorithm = "HS256")
#         response = Response()

#         response.set_cookie(key = 'jwt', value = token, httponly = True)
#         response.data = {'jwt': token, "valid_user":True }

#         return response


# class GetUser(APIView):
#     def get(self, request):
#         response = ValidateUser(request)
#         if response["valid_user"]:
#             data = UserSerializer(response['user'])
#             return Response({"user": data.data, "valid_user":True}, status=status.HTTP_200_OK)

#         return Response(response, status=status.HTTP_200_OK)


# class LogoutUser(APIView):
#     def post(self, request):
#         response = Response()
#         response.delete_cookie('jwt')
#         response.data = {
#             "mesagge":"Sesión cerrada"
#         }
#         return response    


# class UpdateUser(APIView):
#     def put(sefl, request):
#         return Response({'message': 'Usuario actualizado correctamente'}, status=status.HTTP_200_OK)


# class DeleteUser(APIView):
#     def delete():
#         pass

# class ChangePasswordUser(APIView):
#     def post(self, request):
#         user = ValidateUser(request)

#         serializer = ChangePasswordSerializer(data=request.data)

#         if serializer.is_valid():
#             old_password = serializer.data.get("old_password")
#             new_password = serializer.data.get("new_password")

#             if not user.check_password(old_password):
#                 return Response({"old_password": ["Contraseña actual incorrecta."]}, status=status.HTTP_400_BAD_REQUEST)

#             user.set_password(new_password)
#             user.save()
#             return Response({"message": "Contraseña cambiada exitosamente."}, status=status.HTTP_200_OK)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def ValidateUser(request):       
#         token = request.COOKIES.get('jwt')
#         if not token:
#             return {"user": "Usuario no autenticado", "valid_user": False}
#         try:
#             payload = jwt.decode(token,'secret', algorithms = ['HS256'])
#         except jwt.ExpiredSignatureError:
#             return {"user": "Usuario no autenticado", "valid_user" :False}
#         response = User.objects.get(username=payload['username'])
#         return {"user": response, "valid_user": True}
        

# class ListarUsuariosView(APIView):
#     def get(self, request):
#         usuario = ValidateUser(request)

#         if usuario["valid_user"]:
        
#             vector_uno = self.request.query_params.get('vector_unidades_territoriales' , '')
#             vector_dos = self.request.query_params.get('vector_contratos' , '')
#             vector_unidades_territoriales = vector_uno.split(',')
#             vector_contratos = vector_dos.split(',')
#             kword = self.request.query_params.get('kw' , '')
            
           
#             response = User.objects.filter(
#                 Q(unidades_territoriales__in = vector_unidades_territoriales),
#                 Q(contratos__in = vector_contratos), 
#                 Q(username__icontains = kword ) | Q( assigned__icontains = kword ) | Q( first_name__icontains = kword ) | Q( last_name__icontains = kword ),
#             ).distinct()
            
#             serializer = UserSerializer(response, many=True)
                
#             return Response(serializer.data)
        
#         return Response(usuario)

