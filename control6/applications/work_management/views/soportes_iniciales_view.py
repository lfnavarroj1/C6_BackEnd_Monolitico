from rest_framework import status
from rest_framework.generics import (
    ListAPIView, 
    CreateAPIView, 
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView
    )
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.soportes_iniciales import SoportesIniciales
from ..serializers.soportes_iniciales_serializers import CrearSoportesInciales, SoportesIncialesSerializer
from ..models.trabajo import Trabajo
from rest_framework.exceptions import AuthenticationFailed
import jwt,json, os #, datetime
from ...users.models import User

from django.http import FileResponse, HttpResponse
from django.conf import settings
from ...users.views import ValidateUser
import mimetypes

class SubirArchivoView(APIView):
    def post(self, request, *args, **kwargs):
        user = ValidateUser(request)
        # archivo = request.data.get('archivo')
        
        data = request.data
        id_trabajo = data['trabajo']
        data['trabajo'] = Trabajo.objects.get(pk=id_trabajo)
        serializer = CrearSoportesInciales(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 2. ELIMINAR SOPORTE INICIAL
class EliminarSoporteInicial(DestroyAPIView):
    def post(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
    queryset=SoportesIniciales.objects.all()
    serializer_class=CrearSoportesInciales
    lookup_field='pk'

    def perform_destroy(self, instance):
        if bool(instance.archivo):
            ruta_archivo=os.path.join(settings.MEDIA_ROOT,str(instance.archivo))
            if os.path.exists(ruta_archivo):
                directorio=os.path.dirname(ruta_archivo)
                os.remove(ruta_archivo)
                os.rmdir(directorio)
        
        instance.delete()

# 3. LISTAR SOPORTES ASOCIADOS A UN TRABAJO
class ListarSoportesIniciales(ListAPIView):
    serializer_class=SoportesIncialesSerializer
    def get_queryset(self):
        token=self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        id_control=self.kwargs.get('pk')

        response=SoportesIniciales.objects.filter(trabajo__id_control=id_control).all()
        return response

#4. Descargar el archivo
class DescargaArchivo(RetrieveAPIView):
    serializer_class = SoportesIncialesSerializer
    # queryset = SoportesIniciales.objects.all()  # Establece el queryset directamente en la clase

    def retrieve(self, request, *args, **kwargs):
        try:
            token = self.request.COOKIES.get('jwt')
            if not token:
                raise AuthenticationFailed("No autenticado.")

            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            
            id_archivo = self.kwargs.get('id')
            instance=SoportesIniciales.objects.get(pk=id_archivo)
            file_path = instance.archivo.path

            # Usando python-magyc
            # mime=magic.Magic()
            file_type, encoding = mimetypes.guess_type(file_path)
            print(file_type)

            if os.path.exists(file_path):
                with open(file_path, 'rb') as file:
                    response = HttpResponse(file, content_type= file_type)
                    # response = FileResponse(file)
                    # response['Content-Disposition']='attachment; filename="Soporte"'
                    return response
            else:
                return Response({'error': 'El archivo no existe.'}, status=status.HTTP_404_NOT_FOUND)

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expirado. Vuelve a iniciar sesión.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Token inválido. Vuelve a iniciar sesión.")
        except SoportesIniciales.DoesNotExist:
            raise AuthenticationFailed("Archivo no encontrado.")
        except Exception as e:
            return Response({'error': 'No se puede abrir el archivo.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)