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
import mimetypes
from ..users.views import ValidateUser
# 1. SUBIR LIBRETOS A UN TRABAJO ----------------------------------------------------------------------------
class CargarLibreto(APIView):
    def post(self, request, *args, **kwargs):
        usuario = ValidateUser(request)
        if usuario['valid_user']:
            response = Libreto.objects.all(request.data)
            return response
        return Response(usuario)
# ----------------------------------------------------------------------------------------------------------------------


# 2. LISTAR LIBRETOS DE UN TRABAJO -------------------------------------------------------------------------
class ListarLibreto(APIView):
    def get(self, request,  *args, **kwargs):
        usuario = ValidateUser(request)
        if usuario['valid_user']:
            pk = self.kwargs.get('pk')
            response=Libreto.objects.filter(request.data ,trabajo__id_control=pk).all()
            return response
        return Response(usuario)
# ----------------------------------------------------------------------------------------------------------------------


# 3. OBTENER EL DETALLE DE UN LIBRETO ----------------------------------------
class ObtenerLibreto(APIView):
    def get(self, request, *args, **kwargs):
        usuario = ValidateUser(request)
        if usuario['valid_user']:
            pk = self.kwargs.get('pk')
            queryset = Libreto.objects.filter(request.data ,id_libreto=pk)
            return queryset
        return Response(usuario)
# -------------------------------------------------------------------------------


# 4. ACTUALIZAR UN LIBRETO ------------------------------------------------------
class ActualizarLibreto(APIView):
    def put(self, request, pk):
        usuario = ValidateUser(request)
        if usuario['valid_user']:
            pk = self.kwargs.get('pk')
            response = Libreto.objects.actualizar_libreto(request.data, pk)
            return response
        return Response(usuario)

# -------------------------------------------------------------------------------

# 5.ELIMINAR UN LIBRETO
class EliminarLibreto(APIView):
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


    