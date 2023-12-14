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
from ...static_data.serializers.proceso_serializer import ProcesoSerializer,ConteoProcesoSerializer
from ..serializers.valorizacion_serializer import ValorizacionSerializer
from ...static_data.serializers.ruta_proceso_serializer import RutaProcesoSerializer

from collections import Counter
# from django.db.models import F
# from django.urls import reverse_lazy
# from ..models.trazabilidad import Trazabilidad
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt,json #, datetime
from rest_framework import status

from ..models.lcl import Lcl
from ..models.valorizacion import Valorizacion
from ..models.odm import Odm

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

        # print(request.data)
        
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
        ruta=RutaProceso.objects.filter(proceso=trabajo.proceso)
        ruta_arreglo=[
            {
                'paso':r.paso,
                'estado':r.estado.id_estado,
            }
            for r in ruta]

        paso_maximo=ruta.count()
        paso_actual=trabajo.ruta_proceso.paso
        estado_actual=trabajo.ruta_proceso.estado
        paso_siguiente=int(paso_actual)+1

        # Validar que el paso máximo no supere
        if paso_siguiente>paso_maximo:
            return Response({'message':  "El trabajo se encuentra en su estado máximo"}, status=205)

        arreglo_siguiente_paso=[item for item in ruta_arreglo if item["paso"]==str(paso_siguiente)]
        estado_siguiente=arreglo_siguiente_paso[0]["estado"]
        
        # Estados E01 a E02

        # Estados E02 a E03
        if estado_actual.id_estado=="E02" and estado_siguiente=="E03":
            valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
            if not valorizaciones.exists():
                return Response({'message':  "El trabajo no tiene valorizaciones cargadas"}, status=205)
            
        # Estados E03 a E04
        if estado_actual.id_estado=="E03" and estado_siguiente=="E04":
            valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
            ser_val=[val.estado for val in valorizaciones]
            if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
                return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)

        # Estados E04 a E05
        if estado_actual.id_estado=="E04" and estado_siguiente=="E05":
            odms=Odm.objects.obtener_odms(pk)
            if not odms.exists():
                return Response({'message':  "El trabajo no tiene odms activas"}, status=205)

        # Estados E05 a E06 --> Para pasar de E5 a E6 requiere almenos una LCL asignada en estado LIBERACION OPERATIVA.
        if estado_actual.id_estado=="E05" and estado_siguiente=="E06":
            lcls=Lcl.objects.obtener_lcls(pk)
            arr_lcl=[lcl.estado_lcl for lcl in lcls]
            if not lcls.exists() or any(valor!="0" for valor in arr_lcl):
                return Response({'message':  "El trabajo no tiene lcls activas en liberación operativa"}, status=205)

        # Estados E06 a E07
        if estado_actual.id_estado=="E06" and estado_siguiente=="E07":
            lcls=Lcl.objects.obtener_lcls(pk)
            arr_lcl=[lcl.estado_lcl for lcl in lcls]
            if not lcls.exists() or not any(valor=="1" for valor in arr_lcl):####
                return Response({'message':  "El trabajo debe tener almenos una LCL liberada"}, status=205)
            
        # # Estados E07 a E08
        # if estado_actual.id_estado=="E07" and estado_siguiente=="E08":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)
            
        # # Estados E08 a E09
        # if estado_actual.id_estado=="E08" and estado_siguiente=="E09":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)
            
        # # Estados E09 a E10
        # if estado_actual.id_estado=="E09" and estado_siguiente=="E10":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)
            

        # # Estados E10 a E11
        # if estado_actual.id_estado=="E10" and estado_siguiente=="E11":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)
            

        # # Estados E11 a E12
        # if estado_actual.id_estado=="E11" and estado_siguiente=="E12":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)
            

        # # Estados E12 a E13
        # if estado_actual.id_estado=="E12" and estado_siguiente=="E13":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)
            

        # # Estados E13 a E14
        # if estado_actual.id_estado=="E13" and estado_siguiente=="E14":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)
            

        # # Estados E14 a E15
        # if estado_actual.id_estado=="E14" and estado_siguiente=="E15":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)
            

        # # Estados E15 a E16
        # if estado_actual.id_estado=="E15" and estado_siguiente=="E16":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)
            

        # # Estados E16 a E17
        # if estado_actual.id_estado=="E16" and estado_siguiente=="E17":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)
            

        # # Estados E17 a E18
        # if estado_actual.id_estado=="E17" and estado_siguiente=="E18":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)


        try:
            if paso_maximo < paso_siguiente:
                raise NoTienSiguienteEstado
            datos_actualizacion={"ruta_proceso":RutaProceso.objects.get(proceso=trabajo.proceso, paso=paso_siguiente)}
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
        ruta=RutaProceso.objects.filter(proceso=trabajo.proceso)
        ruta_arreglo=[
            {
                'paso':r.paso,
                'estado':r.estado.id_estado,
            }
            for r in ruta]

        paso_actual=trabajo.ruta_proceso.paso
        estado_actual=trabajo.ruta_proceso.estado
        paso_siguiente=int(paso_actual)-1

        # Validar que el paso mínimo no supere
        if 1 > paso_siguiente:
            return Response({'message':  "El trabajo se encuentra en su estado mínimo"}, status=205)

        arreglo_siguiente_paso=[item for item in ruta_arreglo if item["paso"]==str(paso_siguiente)]
        estado_siguiente=arreglo_siguiente_paso[0]["estado"]
        
        # Estados E02 a E01

        # Estados E03 a E02
        if estado_actual.id_estado=="E03" and estado_siguiente=="E02":
            valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
            if valorizaciones.exists():
                return Response({'message':  "El trabajo tiene valorizaciones cargadas"}, status=205)
            
        # Estados E04 a E03
        if estado_actual.id_estado=="E04" and estado_siguiente=="E03":
            valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
            ser_val=[val.estado for val in valorizaciones]
            if any(valor !="1" for valor in ser_val):
                return Response({'message':  "El trabajo no tiene valorizaciones rechazada"}, status=205)

        # Estados E05 a E04
        if estado_actual.id_estado=="E05" and estado_siguiente=="E04":
            odms=Odm.objects.obtener_odms(pk)
            if odms.exists():
                return Response({'message':  "El trabajo tiene odms activas"}, status=205)

        # Estados E06 a E05 --> Para pasar de E5 a E6 requiere almenos una LCL asignada en estado LIBERACION OPERATIVA.
        if estado_actual.id_estado=="E06" and estado_siguiente=="E05":
            lcls=Lcl.objects.obtener_lcls(pk)
            if lcls.exists() :
                return Response({'message':  "El trabajo tiene lcls activas"}, status=205)

        # Estados E07 a E06
        if estado_actual.id_estado=="E06" and estado_siguiente=="E07":
            lcls=Lcl.objects.obtener_lcls(pk)
            if lcls.exists():
                return Response({'message':  "El trabajo tiene lcls activas"}, status=205)
            
        # # Estados E08 a E07
        # if estado_actual.id_estado=="E07" and estado_siguiente=="E08":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)
            
        # # Estados E09 a E08
        # if estado_actual.id_estado=="E08" and estado_siguiente=="E09":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)
            
        # # Estados E10 a E09
        # if estado_actual.id_estado=="E09" and estado_siguiente=="E10":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)
            

        # # Estados E11 a E10
        # if estado_actual.id_estado=="E10" and estado_siguiente=="E11":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)
            

        # # Estados E12 a E11
        # if estado_actual.id_estado=="E11" and estado_siguiente=="E12":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)
            

        # # Estados E13 a E12
        # if estado_actual.id_estado=="E12" and estado_siguiente=="E13":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)
            

        # # Estados E14 a E13
        # if estado_actual.id_estado=="E13" and estado_siguiente=="E14":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)
            

        # # Estados E15 a E14
        # if estado_actual.id_estado=="E14" and estado_siguiente=="E15":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)
            

        # # Estados E16 a E15
        # if estado_actual.id_estado=="E15" and estado_siguiente=="E16":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)
            

        # # Estados E17 a E16
        # if estado_actual.id_estado=="E16" and estado_siguiente=="E17":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)
            

        # # Estados E18 a E17
        # if estado_actual.id_estado=="E17" and estado_siguiente=="E18":
        #     valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
        #     ser_val=[val.estado for val in valorizaciones]
        #     if not valorizaciones.exists() or all(valor =="0" for valor in ser_val):
        #         return Response({'message':  "El trabajo no tiene valorizaciones aprobada"}, status=205)



        # Estado (E6)
        # Validar si se tiene una lcl 
        lcls=Lcl.objects.obtener_lcls(pk)

        if lcls:
            return Response({'message':  "El trabajo actual tiene LCL's activas"}, status=205)


        try:
            if 1 > paso_siguiente:
                raise NoTienSiguienteEstado
            datos_actualizacion={"ruta_proceso":RutaProceso.objects.get(proceso=trabajo.proceso, paso=paso_siguiente)}
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


# 8. CONTAR TRABAJOS POR PROCESO ------------------------------------
class ContarTrabajosPorProcesos(APIView):
    # serializer_class=ProcesoSerializer
    def get(self,request):
        token=request.COOKIES.get('jwt')
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
        
        response=Trabajo.objects.contar_trabajos_procesos(vect_procesos,vect_estados,kword)
        serializer=TrabajoSerializer(response,many=True)
        procesos=[proceso['proceso'] for proceso in serializer.data]
        nombre_procesos=[proc['nombre'] for proc in procesos]
        conteo_nombre_procesos=Counter(nombre_procesos)
        return Response(conteo_nombre_procesos, status=200)
# ---------------------------------------------------------------------


# 9. CONTAR TRABAJOS POR ESTADOS ------------------------------------------
class ContarTrabajosPorEstado(APIView):
     def get(self,request):
        token=request.COOKIES.get('jwt')
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
        
        response=Trabajo.objects.contar_trabajos_procesos(vect_procesos,vect_estados,kword)
        serializer=TrabajoSerializer(response,many=True)
        ruta=[rut['ruta_proceso'] for rut in serializer.data]
        estados=[est['estado'] for est in ruta]
        id_estados=[est['id_estado'] for est in estados]
        conteo_id_estado=Counter(id_estados)

        return Response(conteo_id_estado, status=200)

# # ---------------------------------------------------------------------
