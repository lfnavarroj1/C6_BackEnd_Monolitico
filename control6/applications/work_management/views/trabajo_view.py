from rest_framework.generics import (
    ListAPIView, 
    CreateAPIView, 
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView
    )
from rest_framework.views import APIView
from ..models.trabajo import Trabajo
from ..models.trazabilidad import Trazabilidad
from ...users.models import User
from ..serializers.trabajo_serializer import TrabajoSerializer, CrearTrabajoSerializer

# from django.db.models import F
# from django.urls import reverse_lazy
# from ..models.trazabilidad import Trazabilidad
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt,json #, datetime
from rest_framework import status

from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from ...static_data.models.ruta_proceso import RutaProceso

from ..errores import CampoRequeridoError, NoTienSiguienteEstado

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
        
        vp1=self.request.query_params.get('vp','')
        ve1=self.request.query_params.get('ve','')
        kword=self.request.query_params.get('kw','')
        vect_procesos=vp1.split(',')
        vect_estados=ve1.split(',')
        
        response=Trabajo.objects.filtrar_trabajos(vect_procesos,vect_estados,kword)
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
        
        usuario=User.objects.get(username=payload['username'])

        print(request.data)
        
        try:
            response=Trabajo.objects.crear_trabajo(request.data)
            datos={}
            datos["trabajo"]=response.id_control
            datos["comentario_trazabilidad"]=f"Trabajo {response.id_control} creado en estado {response.ruta_proceso.estado.nombre}"
            Trazabilidad.objects.registrar_trazabilidad(datos, usuario)
            return Response({'message': f'Trabajo {response.id_control} creado exitosamente'}, status=201)
        except CampoRequeridoError as e:
            mensaje = str(e)
            status_code = e.status_code
            return Response({'error': mensaje}, status=status_code)

# # ---------------------------------------------------------------------

# 3. ACTUALIZAR UN TRABAJO -----------------------------------------------
class ActualizarTrabajo(UpdateAPIView):
    def put(self, request, pk):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        usuario=User.objects.get(username=payload['username'])
        pk = self.kwargs.get('pk')

        try:
            response=Trabajo.objects.actualizar_trabajo(request.data, pk)
            dic=request.data
            campos_actualizados=""
            for campo in dic.keys():
                campos_actualizados=campos_actualizados +", "+campo
            
            datos={}
            datos["trabajo"]=response.id_control
            datos["comentario_trazabilidad"]=f"Se actualizaron los campos {campos_actualizados} del trabajo {response.id_control}"
            Trazabilidad.objects.registrar_trazabilidad(datos, usuario)
            return Response({'message':  datos["comentario_trazabilidad"]}, status=201)
        except CampoRequeridoError as e:
            mensaje = str(e)
            status_code = e.status_code
            return Response({'error': mensaje}, status=status_code)
# ---------------------------------------------------------------------


# # 3.1 ACTUAIZAR ALGUNOS CAMPOS DEL TRABAJO
# class ActualizarParcialTrabajo(UpdateAPIView):
#     def post(self, request):
#         token=request.COOKIES.get('jwt')
#         if not token:
#             raise AuthenticationFailed("Unauthenticated!")
#         try:
#             payload=jwt.decode(token,'secret',algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed("Unauthenticated!")
        
#     class Meta:
#         model=Trabajo
#         fields=(
#             'pms_quotation',
#             'pms_need',
#             'proceso',
#             'caso_radicado',
#             'estado_trabajo',
#             'alcance',
#             'estructura_presupuestal',
#             'priorizacion',
#             'unidad_territorial',
#             'municipio',
#             'vereda',
#             'direccion',
#             'subestacion',
#             'circuito',
#             'contrato',
#         )
#     queryset=Trabajo.objects.all()
#     serializer_class=CrearTrabajoSerializer
#     lookup_field='pk'

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
class SiguienteEstado(UpdateAPIView):
    def put(self, request, pk):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        usuario=User.objects.get(username=payload['username'])
        pk = self.kwargs.get('pk')

        # Cambio de estado
        
        trabajo=Trabajo.objects.get(id_control=pk)
        numero_maximo=RutaProceso.objects.filter(proceso=trabajo.proceso).count()
        estado_actual=trabajo.ruta_proceso.paso
        estado_siguiente=int(estado_actual)+1
        

        try:
            if numero_maximo < estado_siguiente:
                raise NoTienSiguienteEstado
            datos_actualizacion={"ruta_proceso":RutaProceso.objects.get(proceso=trabajo.proceso, paso=estado_siguiente)}
            response=Trabajo.objects.actualizar_trabajo(datos_actualizacion, pk)
            campos_actualizados=datos_actualizacion['ruta_proceso']
            
            datos={}
            datos["trabajo"]=response.id_control
            datos["comentario_trazabilidad"]=f"Se cambiado al estado del trabajo {response.id_control} a {campos_actualizados.estado.nombre}"
            Trazabilidad.objects.registrar_trazabilidad(datos, usuario)
            return Response({'message':  datos["comentario_trazabilidad"]}, status=201)
        except CampoRequeridoError as e:
            mensaje = str(e)
            status_code = e.status_code
            return Response({'error': mensaje}, status=status_code)
        except NoTienSiguienteEstado as e:
            mensaje = str(e)
            status_code = e.status_code
            return Response({'error': mensaje}, status=status_code)
        
# ---------------------------------------------------------------------

# 6. ESTADO ANTERIOR
class AnteriorEstado(UpdateAPIView):
    def put(self, request, pk):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        usuario=User.objects.get(username=payload['username'])
        pk = self.kwargs.get('pk')

        # Cambio de estado
        
        trabajo=Trabajo.objects.get(id_control=pk)
        estado_actual=trabajo.ruta_proceso.paso
        estado_siguiente=int(estado_actual)-1
        

        try:
            if 1 > estado_siguiente:
                raise NoTienSiguienteEstado
            datos_actualizacion={"ruta_proceso":RutaProceso.objects.get(proceso=trabajo.proceso, paso=estado_siguiente)}
            response=Trabajo.objects.actualizar_trabajo(datos_actualizacion, pk)
            campos_actualizados=datos_actualizacion['ruta_proceso']
            
            datos={}
            datos["trabajo"]=response.id_control
            datos["comentario_trazabilidad"]=f"Se cambiado al estado del trabajo {response.id_control} a {campos_actualizados.estado.nombre}"
            Trazabilidad.objects.registrar_trazabilidad(datos, usuario)
            return Response({'message':  datos["comentario_trazabilidad"]}, status=201)
        except CampoRequeridoError as e:
            mensaje = str(e)
            status_code = e.status_code
            return Response({'error': mensaje}, status=status_code)
        except NoTienSiguienteEstado as e:
            mensaje = str(e)
            status_code = e.status_code
            return Response({'error': mensaje}, status=status_code)
# ---------------------------------------------------------------------

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