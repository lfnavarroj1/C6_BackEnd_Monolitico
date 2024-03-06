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
from .models import Libreto
from .serializers import CrearLibretoSerializer, LibretoSerializer
from ..work_management.models import Trabajo
from ..lcl_management.models import Lcl
from ..scheduling_management.models import Programacion
from rest_framework.exceptions import AuthenticationFailed
import jwt,json, os #, datetime
from ..users.models import User

from django.http import FileResponse, HttpResponse
from django.conf import settings
# import magic
import mimetypes

from ..users.views import ValidateUser


class CrearLibretoView(APIView):
    def post(self, request, *args, **kwargs):
        usuario = ValidateUser(request)
        
        if usuario["valid_user"]:
            serializer = CrearLibretoSerializer(data = request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(usuario)


class ListarLibretosTrabajoView(ListAPIView):
    serializer_class=LibretoSerializer
    def get_queryset(self):
        token=self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Usuario no autenticado")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Usuario no autenticado")
        
        id_control=self.kwargs.get('pk')
        response=Libreto.objects.filter(trabajo__id_control=id_control).all()
        return response


class ObtenerDetalleLibretoView(RetrieveAPIView):
    serializer_class = LibretoSerializer

    def get_queryset(self):
        token = self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Usuario no autenticado")

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Usuario no autenticado")

        # Obtiene el parámetro de la URL 'pk' para buscar el trabajo específico
        pk = self.kwargs.get('pk')
        queryset = Libreto.objects.filter(id_libreto=pk)

        return queryset


class ActualizarLibretoView(UpdateAPIView):
    def put(self, request, pk):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Usuario no autenticado")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Usuario no autenticado")

        # usuario=User.objects.get(username=payload['username'])
        pk = self.kwargs.get('pk')

        print(request.data)

        try:
            response=Libreto.objects.actualizar_libreto(request.data, pk)
            return Response({'message': f'El presupuesto {response} fue actualizados'}, 200)
        except Exception as e:
            mensaje = str(e)
            status_code = 412  #e.status_code
            return Response({'error': mensaje}, status=status_code)


class EliminarLibretoView(DestroyAPIView):
    def put(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Usuario no autenticado")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Usuario no autenticado")
        
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


    