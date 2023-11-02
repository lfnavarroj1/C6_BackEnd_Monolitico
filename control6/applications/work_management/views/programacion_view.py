from rest_framework.generics import (
    ListAPIView, 
    CreateAPIView, 
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView
    )
from rest_framework.views import APIView
from ..models.programacion import Programacion
from ..serializers.programacion_serializer import ProgramacionSerializer,CrearProgramacionSerializer
from ...users.models import User
from ...static_data.serializers.cuadrilla_serializer import CuadrillaSerializer
from ...static_data.models.cuadrilla import Cuadrilla


# from django.db.models import F
# from django.urls import reverse_lazy
# from ..models.trazabilidad import Trazabilidad
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt #, datetime
from rest_framework import status

from rest_framework.response import Response
from rest_framework.exceptions import NotFound


# 1. CREAR PROGRAMACION ----------------------------------------
class CrearProgramacion(CreateAPIView):
    serializer_class=CrearProgramacionSerializer
    def post(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        response=Programacion.objects.registrar_programacion(request.data)
        return response
# ---------------------------------------------------------------------


# 2. LISTAR PROGRAMACIONES ASOCIADAS A UN TRABAJO --------------------------------
class ListarProgramacion(ListAPIView):
    serializer_class=ProgramacionSerializer
    def get_queryset(self):
        token=self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        

        pk = self.kwargs.get('pk')
        queryset=Programacion.objects.obtener_programacion(pk)
        return queryset
# ---------------------------------------------------------------------

# 2.1 LISTAR CUADRILLAS DISPONIBLES EN UNA FECHA ----------------------
class ListarCuadrillasDisponibles(ListAPIView):
    serializer_class=CuadrillaSerializer
    # serializer_class=ProgramacionSerializer
    def get_queryset(self):
        token=self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        lista_cuadrillas=set(list(Cuadrilla.objects.all()))
        # print(lista_cuadrillas)
        date = self.kwargs.get('date')
        programacion_fecha=Programacion.objects.filter(fecha_ejecucion=date)
        # cuadrillas=programacion_fecha.cuadrillas
        cuadrillas_programadas_fecha=[]


        for programacion in programacion_fecha:
            cuadrillas=programacion.cuadrillas.all()
            cuadrillas_programadas_fecha.append(list(cuadrillas))

        lista_programada=set([cuadrilla for list in cuadrillas_programadas_fecha for cuadrilla in list])
        lista_disponible=list(lista_cuadrillas.difference(lista_programada))

        # print(lista_disponible)

        # print(cudrillas_programadas_fecha)
        # queryset=Programacion.objects.filter(fecha_ejecucion=date)
        queryset=list(lista_cuadrillas.difference(lista_programada))
        return queryset
# ---------------------------------------------------------------------


# 3. OBTENER DETALLES DE UNA ODM ASOCIADAS A UN TRABAJO ---------------
class ObtenerProgramacion(RetrieveAPIView):
    serializer_class = ProgramacionSerializer

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
        queryset = Programacion.objects.filter(id_programcion=pk)
        return queryset
# ---------------------------------------------------------------------


# 4. ACTUALIZAR ODM ASOCIADAS A UN TRABAJO ----------------------------
class ActualizarProgramacion(UpdateAPIView):
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
            response=Programacion.objects.actualizar_programacion(request.data, pk)
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
            return Response({'error': mensaje}, status=401)
# ---------------------------------------------------------------------


# 5. ELIMINAR ODM ASOCIADAS A UN TRABAJO ------------------------------
class EliminarProgramacion(DestroyAPIView):
    def post(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
    queryset=Programacion.objects.all()
    serializer_class=ProgramacionSerializer
    lookup_field='pk'
# ---------------------------------------------------------------------