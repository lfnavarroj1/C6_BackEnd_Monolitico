from rest_framework.generics import (
    ListAPIView, 
    CreateAPIView, 
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView
    )

from ..models.lcl import Lcl
from ..serializers.lcl_serializer import LclSerializer
from ...users.models import User
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

# 1. CREAR LCL ----------------------------------------
class CrearLcl(CreateAPIView):
    serializer_class=LclSerializer
    def post(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        usuario=User.objects.get(username=payload['username'])
        
        response=Lcl.objects.registrar_lcl(request.data,usuario)
        return response
    
# ---------------------------------------------------------------------


# 2. LISTAR ODM ASOCIADAS A UN TRABAJO --------------------------------
class ListarLcl(ListAPIView):
    serializer_class=LclSerializer
    def get_queryset(self):
        token=self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        pk = self.kwargs.get('pk')
        queryset=Lcl.objects.obtener_lcls(pk)
        return queryset
# ---------------------------------------------------------------------


# 3. OBTENER DETALLES DE UNA ODM ASOCIADAS A UN TRABAJO ---------------
class ObtenerLcl(RetrieveAPIView):
    serializer_class = LclSerializer

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
        queryset = Lcl.objects.filter(lcl=pk)
        return queryset
# ---------------------------------------------------------------------


# 4. ACTUALIZAR ODM ASOCIADAS A UN TRABAJO ----------------------------
class ActualizarLcl(UpdateAPIView):
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
            response=Lcl.objects.actualizar_lcl(request.data, pk)
            # dic=request.data
            # campos_actualizados=""
            # for campo in dic.keys():
            #     campos_actualizados=campos_actualizados +", "+campo
            
            # datos={}
            # datos["trabajo"]=response.id_control
            # datos["comentario_trazabilidad"]=f"Se actualizaron los campos {campos_actualizados} del trabajo {response.id_control}"
            # Odm.objects.registrar_trazabilidad(datos, usuario)
            return Response({'message': f"La {response} fue actualizada"}, status=201)
        except Exception as e:
            mensaje = str(e)
            status_code = e.status_code
            return Response({'error': mensaje}, status=status_code)
# ---------------------------------------------------------------------


# 5. ELIMINAR ODM ASOCIADAS A UN TRABAJO ------------------------------
class EliminarLcl(DestroyAPIView):
    def post(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
    queryset=Lcl.objects.all()
    serializer_class=LclSerializer
    lookup_field='pk'
# ---------------------------------------------------------------------