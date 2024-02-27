from rest_framework.generics import (
    ListAPIView, 
    CreateAPIView, 
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView
    )

from .models import Odm
from .serializers import OdmSerializer
from users.models import User
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

# from rest_framework.views import APIView
#, datetime
# from django.db.models import F
# from django.urls import reverse_lazy
# from ..models.trazabilidad import Trazabilidad

# 1. CREAR ODM ----------------------------------------
class CrearOdm(CreateAPIView):
    serializer_class=OdmSerializer
    def post(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        
        response=Odm.objects.registrar_odm(request.data)
        return response
# ---------------------------------------------------------------------


# 2. LISTAR ODM ASOCIADAS A UN TRABAJO --------------------------
class ListarOdm(ListAPIView):
    serializer_class=OdmSerializer
    def get_queryset(self):
        token=self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        pk = self.kwargs.get('pk')
        queryset=Odm.objects.obtener_odms(pk)
        return queryset
# ---------------------------------------------------------------------


# 3. OBTENER DETALLES DE UNA ODM ASOCIADAS A UN TRABAJO ---------------
class ObtenerOdm(RetrieveAPIView):
    serializer_class = OdmSerializer

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
        queryset = Odm.objects.filter(odm=pk)
        return queryset
# ---------------------------------------------------------------------


# 4. ACTUALIZAR ODM ASOCIADAS A UN TRABAJO ----------------------------
class ActualizarOdm(UpdateAPIView):
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
            response=Odm.objects.actualizar_odm(request.data, pk)
            # dic=request.data
            # campos_actualizados=""
            # for campo in dic.keys():
            #     campos_actualizados=campos_actualizados +", "+campo
            
            # datos={}
            # datos["trabajo"]=response.id_control
            # datos["comentario_trazabilidad"]=f"Se actualizaron los campos {campos_actualizados} del trabajo {response.id_control}"
            # Odm.objects.registrar_trazabilidad(datos, usuario)
            return Response({'message': f"La ODM {response} fue actualizada"}, status=201)
        except Exception as e:
            mensaje = str(e)
            status_code = e.status_code
            return Response({'error': mensaje}, status=status_code)
# ---------------------------------------------------------------------


# 5. ELIMINAR ODM ASOCIADAS A UN TRABAJO ------------------------------
class EliminarOdm(DestroyAPIView):
    def post(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
    queryset=Odm.objects.all()
    serializer_class=OdmSerializer
    lookup_field='pk'
# ---------------------------------------------------------------------
