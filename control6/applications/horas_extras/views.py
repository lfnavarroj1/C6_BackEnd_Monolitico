from rest_framework.generics import (
    ListAPIView, 
    CreateAPIView, 
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView
    )

from .serializers import HoraExtraSerializer,CrearHESerializer
from rest_framework.views import APIView
from .models import HoraExtra
from ..users.models import User


# from django.db.models import F
# from django.urls import reverse_lazy
# from ..models.trazabilidad import Trazabilidad
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt #, datetime
from rest_framework import status

from rest_framework.response import Response
from rest_framework.exceptions import NotFound


# 1. CREAR HORAS EXTRAS ----------------------------------------
class CrearHoraExtra(CreateAPIView):
    serializer_class=CrearHESerializer
    def post(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        usuario=User.objects.get(username=payload['username'])
        response=HoraExtra.objects.registrar_hora_extra(request.data,usuario)
        return response
# ---------------------------------------------------------------------


# 2. LISTAR HORAS EXTRAS DE UN USUARIO --------------------------------
class ListarHorasExtras(ListAPIView):
    serializer_class=HoraExtraSerializer
    def get_queryset(self):
        token=self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        usuario=User.objects.get(username=payload['username'])
        
        queryset=HoraExtra.objects.obtener_horas_extras(usuario)
        return queryset
# ---------------------------------------------------------------------

# 3. OBTENER DETALLES DE UNA HORA EXTRA-------------- ---------------
class ObtenerHoraExtra(RetrieveAPIView):
    serializer_class = HoraExtraSerializer

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
        queryset = HoraExtra.objects.filter(id_hora_extra=pk)
        return queryset
# ---------------------------------------------------------------------

# 4. ACTUALIZAR HORA EXTRA ----------------------------
class ActualizarHoraExtra(UpdateAPIView):
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
            response=HoraExtra.objects.actualizar_horas_extras(request.data, pk)
            return Response({'message': f"La {response} fue actualizada"}, status=201)
        except Exception as e:
            mensaje = str(e)
            status_code = e.status_code
            return Response({'error': mensaje}, status=401)
# ---------------------------------------------------------------------


# 5. ELIMINAR HORA EXTRA ----------------------------------------------
class EliminarHoraExtra(DestroyAPIView):
    def post(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
    queryset=HoraExtra.objects.all()
    serializer_class=HoraExtraSerializer
    lookup_field='pk'
# ---------------------------------------------------------------------