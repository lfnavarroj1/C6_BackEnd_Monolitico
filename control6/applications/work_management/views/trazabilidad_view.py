from rest_framework.generics import (
    ListAPIView, 
    CreateAPIView, 
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView
    )
from rest_framework.views import APIView
from ..models.trazabilidad import Trazabilidad
from ..serializers.trazabilidad_serializer import TrazabilidadSerializer
from ...users.models import User

# from django.db.models import F
# from django.urls import reverse_lazy
# from ..models.trazabilidad import Trazabilidad
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt #, datetime
from rest_framework import status

from rest_framework.response import Response
from rest_framework.exceptions import NotFound


# 1.CREAR TRAZABILIDAD ----------------------------------------
class CrearTrazabilidad(CreateAPIView):
    serializer_class=TrazabilidadSerializer
    def post(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        usuario=User.objects.get(username=payload['username'])
        response=Trazabilidad.objects.registrar_trazabilidad(request.data, usuario)
        return response
# ---------------------------------------------------------------------


# 2.LISTAR TRAZABILIDAD ASOCIADAS A UN TRABAJO --------------------------
class ListarTrazabilidad(ListAPIView):
    serializer_class=TrazabilidadSerializer
    def get_queryset(self):
        token=self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        pk = self.kwargs.get('pk')
        queryset=Trazabilidad.objects.obtener_trazabilidad(pk)
        return queryset
# ---------------------------------------------------------------------