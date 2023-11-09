from rest_framework.generics import (
    ListAPIView, 
    CreateAPIView, 
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView
    )
from rest_framework.views import APIView
from ..models.maniobra import Maniobra
from ..serializers.maniobra_serializer import ManiobraSerializer
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


# 1. CREAR PROGRAMACION -------------------------------------------------
class CrearManiobra(CreateAPIView):
    serializer_class=ManiobraSerializer
    def post(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        response=Maniobra.objects.registrar_maniobra(request.data)
        return response
# ----------------------------------------------------------------------


# 2. LISTAR PROGRAMACIONES ASOCIADAS A UN TRABAJO --------------------------------
class ListarManiobras(ListAPIView):
    serializer_class=ManiobraSerializer
    def get_queryset(self):
        token=self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        pk = self.kwargs.get('pk')
        queryset=Maniobra.objects.obtener_maniobras(pk)
        return queryset
# ---------------------------------------------------------------------


# 3. OBTENER DETALLES DE UNA ODM ASOCIADAS A UN TRABAJO ---------------
class ObtenerManiobra(RetrieveAPIView):
    serializer_class = ManiobraSerializer

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
        queryset = Maniobra.objects.filter(maniobra=pk)
        return queryset
# ---------------------------------------------------------------------


# 4. ACTUALIZAR ODM ASOCIADAS A UN TRABAJO ----------------------------
class ActualizarManiobra(UpdateAPIView):
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
            response=Maniobra.objects.actualizar_maniobra(request.data, pk)
            return Response({'message': f"La {response} fue actualizada"}, status=201)
        except Exception as e:
            mensaje = str(e)
            status_code = 400
            return Response({'error': mensaje}, status=status_code)
# ---------------------------------------------------------------------


# 5. ELIMINAR ODM ASOCIADAS A UN TRABAJO ------------------------------
class EliminarManiobra(DestroyAPIView):
    def post(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
    queryset=Maniobra.objects.all()
    serializer_class=ManiobraSerializer
    lookup_field='pk'
# ---------------------------------------------------------------------