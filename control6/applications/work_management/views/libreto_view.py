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
from ..models.libreto import Libreto
from ..serializers.libreto_serializer import CrearLibretoSerializer, LibretoSerializer
from ..models.trabajo import Trabajo
from ..models.programacion import Programacion
from rest_framework.exceptions import AuthenticationFailed
import jwt,json, os #, datetime
from ...users.models import User

from django.http import FileResponse, HttpResponse
from django.conf import settings

# import magic
import mimetypes

# 1. SUBIR LIBRETOS A UN TRABAJO ----------------------------------------------------------------------------
class CargarLibreto(APIView):
    def post(self, request, *args, **kwargs):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        # usuario=User.objects.get(username=payload['username'])
        # presupuesto = request.data.get('presupuesto') 

        # Crear una instancia del modelo SoportesIniciales con el archivo
        data=request.data
        prog=data['programacion']
        tra=data['trabajo']

        data['programacion']=Programacion.objects.get(pk=prog)
        data['trabajo']=Trabajo.objects.get(pk=tra)

        # Este es un ejemplo de como accedder o navegar entre tablas relacionadas habilitar para acceder.
        # print(data['programacion'].lcl.odms.all()[0].valorizacion.trabajo)

        serializer = CrearLibretoSerializer(data=request.data)

        if serializer.is_valid():
            # Guardar el archivo en el modelo SoportesIniciales
            serializer.save()

            # Devolver una respuesta de éxito
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Si hay errores de validación, devolver una respuesta con los errores
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ----------------------------------------------------------------------------------------------------------------------


# 2. LISTAR LIBRETOS DE UN TRABAJO -------------------------------------------------------------------------
class ListarLibreto(ListAPIView):
    serializer_class=LibretoSerializer
    def get_queryset(self):
        token=self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        id_control=self.kwargs.get('pk')
        response=Libreto.objects.filter(trabajo__id_control=id_control).all()
        return response
# ----------------------------------------------------------------------------------------------------------------------


# 3. OBTENER EL DETALLE DE UN LIBRETO ----------------------------------------
class ObtenerLibreto(RetrieveAPIView):
    serializer_class = LibretoSerializer

    def get_queryset(self):
        token = self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        # Obtiene el parámetro de la URL 'pk' para buscar el trabajo específico
        pk = self.kwargs.get('pk')
        queryset = Libreto.objects.filter(id_libreto=pk)
        return queryset
# -------------------------------------------------------------------------------


# 4. ACTUALIZAR UN LIBRETO ------------------------------------------------------
class ActualizarLibreto(UpdateAPIView):
    def put(self, request, pk):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        # usuario=User.objects.get(username=payload['username'])
        pk = self.kwargs.get('pk')

        try:
            response=Libreto.objects.actualizar_libreto(request.data, pk)
            return Response({'message': f'El presupuesto {response} fue actualizados'}, 200)
        except Exception as e:
            mensaje = str(e)
            status_code = 412  #e.status_code
            return Response({'error': mensaje}, status=status_code)

# -------------------------------------------------------------------------------

# 5.ELIMINAR UN LIBRETO
class EliminarLibreto(DestroyAPIView):
    def put(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
    queryset=Libreto.objects.all()
    serializer_class=LibretoSerializer
    lookup_field='pk'

    def perform_destroy(self, instance):
        if bool(instance.planillas_conciliacion):
            ruta_archivo=os.path.join(settings.MEDIA_ROOT,str(instance.planillas_conciliacion))
            if os.path.exists(ruta_archivo):
                directorio=os.path.dirname(ruta_archivo)
                os.remove(ruta_archivo)
                os.rmdir(directorio)
        
        if bool(instance.planillas_firmadas):
            ruta_archivo=os.path.join(settings.MEDIA_ROOT,str(instance.planillas_firmadas))
            if os.path.exists(ruta_archivo):
                directorio=os.path.dirname(ruta_archivo)
                os.remove(ruta_archivo)
                os.rmdir(directorio)
        
        instance.delete()


    