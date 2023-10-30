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
from ..models.valorizacion import Valorizacion
from ..serializers.valorizacion_serializer import CrearValorizacion, ValorizacionSerializer
from ..models.trabajo import Trabajo
from rest_framework.exceptions import AuthenticationFailed
import jwt,json, os #, datetime
from ...users.models import User

from django.http import FileResponse, HttpResponse
from django.conf import settings

import magic
import mimetypes

# 1. SUBIR SOPORTES INICIALES ASOCIADOS A UN TRABAJO ----------------------------------------------------------------------------
class CargarValorizacionView(APIView):
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
        id_trabajo=data['trabajo']
        data['trabajo']=Trabajo.objects.get(pk=id_trabajo)

        serializer = CrearValorizacion(data=request.data)

        if serializer.is_valid():
            # Guardar el archivo en el modelo SoportesIniciales
            serializer.save()

            # Devolver una respuesta de éxito
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Si hay errores de validación, devolver una respuesta con los errores
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ----------------------------------------------------------------------------------------------------------------------


# 2. LISTAR PRESUPUESTOS CARGADOS A UN TRABAJO -------------------------------------------------------------------------
class ListarValorizacion(ListAPIView):
    serializer_class=ValorizacionSerializer
    def get_queryset(self):
        token=self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        id_control=self.kwargs.get('pk')
        response=Valorizacion.objects.filter(trabajo__id_control=id_control).all()
        return response
# ----------------------------------------------------------------------------------------------------------------------


# 3. OBTENER EL DETALLE DE UN PRESUPUESTO ----------------------------------------
class ObtenerValorizacion(RetrieveAPIView):
    serializer_class = ValorizacionSerializer

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
        queryset = Valorizacion.objects.filter(id_valorizacion=pk)
        return queryset
# -------------------------------------------------------------------------------


# 4. ACTUALIZAR UN PRESUPUESTO ------------------------------------------------------
class ActualizarValorizacion(UpdateAPIView):
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
            response=Valorizacion.objects.actualizar_valorizacion(request.data, pk)
            return Response({'message': f'El presupuesto {response} fue actualizados'}, 200)
        except Exception as e:
            mensaje = str(e)
            status_code = 412  #e.status_code
            return Response({'error': mensaje}, status=status_code)

# -------------------------------------------------------------------------------

# 5.ELIMINAR UN PRESUPUESTO
class EliminarValorizacion(DestroyAPIView):
    def put(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
    queryset=Valorizacion.objects.all()
    serializer_class=ValorizacionSerializer
    lookup_field='pk'

    def perform_destroy(self, instance):
        ruta_archivo=os.path.join(settings.MEDIA_ROOT,str(instance.presupuesto))
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)
        
        instance.delete()