from rest_framework.generics import (
    ListAPIView, 
    CreateAPIView, 
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView
    )
from rest_framework.views import APIView
from ..models.trabajo import Trabajo
from ..serializers.trabajo_serializer import TrabajoSerializer, CrearTrabajoSerializer

# from django.db.models import F
# from django.urls import reverse_lazy
# from ..models.trazabilidad import Trazabilidad
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt #, datetime
from rest_framework import status

from rest_framework.response import Response
from rest_framework.exceptions import NotFound


# 1. LISTAR TRABAJOS ----------------------------------------
class ListarTrabajos(ListAPIView):
    serializer_class=TrabajoSerializer
    def get_queryset(self):
        token=self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        response=Trabajo.objects.lista_trabajos()
        return response
# ---------------------------------------------------------------------


# 2. CREAR UN NUEVO TRABAJO ------------------------------------------------
class CrearTrabajo(CreateAPIView):
    serializer_class=CrearTrabajoSerializer
    def post(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# # ---------------------------------------------------------------------

# 3. ACTUALIZAR UN TRABAJO COMPLETO
class ActualizarTrabajo(UpdateAPIView):
    def post(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
    queryset=Trabajo.objects.all()
    serializer_class=CrearTrabajoSerializer
    lookup_field='pk'
# ---------------------------------------------------------------------


# 3.1 ACTUAIZAR ALGUNOS CAMPOS DEL TRABAJO
class ActualizarParcialTrabajo(UpdateAPIView):
    def post(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
    class Meta:
        model=Trabajo
        fields=(
            'pms_quotation',
            'pms_need',
            'proceso',
            'caso_radicado',
            'estado_trabajo',
            'alcance',
            'estructura_presupuestal',
            'priorizacion',
            'unidad_territorial',
            'municipio',
            'vereda',
            'direccion',
            'subestacion',
            'circuito',
            'contrato',
        )
    queryset=Trabajo.objects.all()
    serializer_class=CrearTrabajoSerializer
    lookup_field='pk'

# 4. ELIMINAR EL TRABAJO
class EliminarTrabajo(DestroyAPIView):
    def post(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
    queryset=Trabajo.objects.all()
    serializer_class=TrabajoSerializer
    lookup_field='pk'

# 5. ESTADO SIGUIENTE


# 6. ESTADO ANTERIOR
    

# 7. OBTENER EL DETALLE DE UN TRABAJO
class ObtenerTrabajo(RetrieveAPIView):
    serializer_class = TrabajoSerializer

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
        queryset = Trabajo.objects.filter(id_control=pk)
        return queryset

# # ---------------------------------------------------------------------


# ALTERNATIVA PERSONALIZADA PARA OBTENER UN TRABAJO
class ObtenerTra(APIView):
    def get(self,request,pk):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        try:
            trabajo=Trabajo.objects.get(id_control=pk)
        except Trabajo.DoesNotExist:
            raise NotFound("El trabajo no existe")
        
        serializer=TrabajoSerializer(trabajo)
        return Response(serializer.data)
# ----------------------------------------------------------------------------