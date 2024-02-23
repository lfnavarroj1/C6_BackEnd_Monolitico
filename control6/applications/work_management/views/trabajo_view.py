from rest_framework import generics
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
from collections import Counter
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, json
from ..models.lcl import Lcl
from ..models.valorizacion import Valorizacion
from ..models.odm import Odm
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from ...static_data.models.ruta_proceso import RutaProceso
from ..errores import CampoRequeridoError, NoTienSiguienteEstado
from ...users.views import ValidateUser
from ..mixins import ValidarCambioEstadoMixin

class ListarTrabajos(generics.ListAPIView):
    serializer_class = TrabajoSerializer
    def get_queryset(self):
        user = ValidateUser(self.request)

        vp1 = self.request.query_params.get('vp' , '')
        ve1 = self.request.query_params.get('ve' , '')
        kword = self.request.query_params.get('kw' , '')
        vect_procesos = vp1.split(',')
        vect_estados  = ve1.split(',')
        
        response = Trabajo.objects.filtrar_trabajos(vect_procesos, vect_estados, kword, user)
        return response

class CrearTrabajo(CreateAPIView):
    serializer_class = CrearTrabajoSerializer
    def post(self, request):        
        usuario = ValidateUser(request)
        
        try:
            response = Trabajo.objects.crear_trabajo(request.data)
            datos={}
            datos["trabajo"]=response.id_control
            datos["comentario_trazabilidad"]=f"Trabajo {response.id_control} creado en estado {response.ruta_proceso.estado.nombre}"
            Trazabilidad.objects.registrar_trazabilidad(datos, usuario)
            return Response({'message': f'Trabajo {response.id_control} creado exitosamente'}, status=201)
        except CampoRequeridoError as e:
            mensaje = str(e)
            status_code = e.status_code
            return Response({'error': mensaje}, status=status_code)

class ActualizarTrabajo(UpdateAPIView):
    def put(self, request, pk):
        usuario = ValidateUser(request)
        pk = self.kwargs.get('pk')

        try:
            response=Trabajo.objects.actualizar_trabajo(request.data, pk)
            dic=request.data
            campos_actualizados=""
            for campo in dic.keys():
                campos_actualizados=campos_actualizados +", "+campo
            
            datos={}
            datos["trabajo"] = response.id_control
            datos["comentario_trazabilidad"] = f"Se actualizaron los campos {campos_actualizados} del trabajo {response.id_control}"
            Trazabilidad.objects.registrar_trazabilidad(datos, usuario)
            return Response({'message':  datos["comentario_trazabilidad"]}, status=201)
        except CampoRequeridoError as e:
            mensaje = str(e)
            status_code = e.status_code
            return Response({'error': mensaje}, status=status_code)

class EliminarTrabajo(DestroyAPIView):
    def post(self, request):
        usuario = ValidateUser(request)
        
    queryset = Trabajo.objects.all()
    serializer_class = TrabajoSerializer
    lookup_field = 'pk'

class SiguienteEstado(UpdateAPIView, ValidarCambioEstadoMixin):
    def put(self, request, pk):
        usuario = ValidateUser(request)
        pk = self.kwargs.get('pk')
        trabajo = Trabajo.objects.get(id_control=pk)
        ruta = RutaProceso.objects.filter(proceso=trabajo.proceso)
        ruta_arreglo = [
            {
                'paso':r.paso,
                'estado':r.estado.id_estado,
            }
            for r in ruta]

        paso_maximo = ruta.count()
        paso_actual = trabajo.ruta_proceso.paso
        estado_actual = trabajo.ruta_proceso.estado
        paso_siguiente = int(paso_actual) + 1

        if paso_siguiente > paso_maximo:
            return Response({'message': "El trabajo se encuentra en su estado máximo"}, status=205)

        arreglo_siguiente_paso = [item for item in ruta_arreglo if item["paso"] == str(paso_siguiente)]
        estado_siguiente = arreglo_siguiente_paso[0]["estado"]

        

        self.validar_cambio_estado(paso_siguiente, estado_actual, estado_siguiente, pk)
        return self.siguiente_estado(trabajo, paso_siguiente, pk, usuario)

    def siguiente_estado(self, trabajo, paso_siguiente, pk, usuario):
        try:
            datos_actualizacion = {"ruta_proceso":RutaProceso.objects.get(proceso=trabajo.proceso, paso=paso_siguiente)}
            response = Trabajo.objects.actualizar_trabajo(datos_actualizacion, pk)
            campos_actualizados = datos_actualizacion['ruta_proceso']
            
            datos={}
            datos["trabajo"] = response.id_control
            datos["comentario_trazabilidad"] = f"Se cambiado al estado del trabajo {response.id_control} a {campos_actualizados.estado.nombre}"
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

        comentario_devolucion=request.data["comentario_devolucion"]
        print(request.data)
        print(comentario_devolucion)

        # Cambio de estado

        trabajo=Trabajo.objects.get(id_control=pk)
        ruta=RutaProceso.objects.filter(proceso=trabajo.proceso)

        # Crear un arreglo con los ID y lo pasos dentro de la ruta
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
        
        
        lcls=Lcl.objects.obtener_lcls(pk)

        if lcls:
            return Response({'message':  "El trabajo actual tiene LCL's activas"}, status=205)


        try:

            datos_actualizacion={"ruta_proceso":RutaProceso.objects.get(proceso=trabajo.proceso, paso=paso_siguiente)}
            response=Trabajo.objects.actualizar_trabajo(datos_actualizacion, pk)
            campos_actualizados=datos_actualizacion['ruta_proceso']
            
            datos={}
            datos["trabajo"]=response.id_control
            datos["comentario_trazabilidad"]=f"Se cambiado al estado del trabajo {response.id_control} a {campos_actualizados.estado.nombre}, con el comentario { comentario_devolucion }"
            # Agregar el comentario de la devolucion siempre.

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

class ObtenerTrabajo(RetrieveAPIView):
    serializer_class = TrabajoSerializer

    def get_queryset(self):

        # token = self.request.COOKIES.get('jwt')
        # if not token:
        #     raise AuthenticationFailed("Unauthenticated!")

        # try:
        #     payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        # except jwt.ExpiredSignatureError:
        #     raise AuthenticationFailed("Unauthenticated!")
        
        usuario = ValidateUser(self.request)

        # Obtiene el parámetro de la URL 'pk' para buscar el trabajo específico
        pk = self.kwargs.get('pk')
        queryset = Trabajo.objects.filter(id_control=pk)
        return queryset

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

class ContarTrabajosPorProcesos(APIView):
    def get(self,request):
        user = ValidateUser(request)
        
        vp1 = self.request.query_params.get('vp','')
        ve1 = self.request.query_params.get('ve','')
        kword = self.request.query_params.get('kw','')
        vect_procesos = vp1.split(',')
        vect_estados = ve1.split(',')
        
        response = Trabajo.objects.contar_trabajos_procesos(vect_procesos, vect_estados, kword, user)
        serializer = TrabajoSerializer(response,many=True)
        procesos = [proceso['proceso'] for proceso in serializer.data]
        nombre_procesos = [proc['nombre'] for proc in procesos]
        conteo_nombre_procesos = Counter(nombre_procesos)
        return Response(conteo_nombre_procesos, status=200)

class ContarTrabajosPorEstado(APIView):
     def get(self,request):
        user = ValidateUser(request)
        
        vp1 = self.request.query_params.get('vp','')
        ve1 = self.request.query_params.get('ve','')
        kword = self.request.query_params.get('kw','')
        vect_procesos = vp1.split(',')
        vect_estados = ve1.split(',')
        
        response = Trabajo.objects.contar_trabajos_procesos(vect_procesos, vect_estados, kword, user)
        serializer = TrabajoSerializer(response,many=True)
        ruta = [rut['ruta_proceso'] for rut in serializer.data]
        estados = [est['estado'] for est in ruta]
        id_estados = [est['id_estado'] for est in estados]
        conteo_id_estado = Counter(id_estados)
        return Response(conteo_id_estado, status=200)

