from rest_framework import generics
from rest_framework.generics import (
    ListAPIView, 
    CreateAPIView, 
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView
)
from rest_framework.views import APIView
from .models import Trabajo, SoportesIniciales
from ..traceability_management.models import TrazabilidadTrabajo
from .serializers import TrabajoSerializer, CrearTrabajoSerializer
from collections import Counter
from rest_framework.response import Response
from .mixins import CambioEstadoTrabajoMixin
from rest_framework import status
from .serializers import CrearSoportesInciales, SoportesIncialesSerializer 
import os 
from django.conf import settings
from ..users.views import ValidateUser
from .errores import CampoRequeridoError
from ..static_data.models.ruta_proceso import RutaProceso


class ListarTrabajos(generics.ListAPIView):
    serializer_class = TrabajoSerializer
    def get_queryset(self):
        user = ValidateUser(self.request)

        if user:
            vp1 = self.request.query_params.get('vp', '')
            ve1 = self.request.query_params.get('ve', '')
            kword = self.request.query_params.get('kw', '')
            vect_procesos = vp1.split(',')
            vect_estados  = ve1.split(',')
        
            response = Trabajo.objects.filtrar_trabajos(vect_procesos, vect_estados, kword, user)
            return response
        response = None
        return response

class CrearTrabajo(CreateAPIView):
    serializer_class = CrearTrabajoSerializer
    def post(self, request):        
        usuario = ValidateUser(request)

        try:
            response = Trabajo.objects.crear_trabajo(request.data)

            if response["creado_exitosamente"]:

                datos = {}
                trabajo = response["trabajo"]
                datos["trabajo"] = trabajo
                datos["comentario_trazabilidad"] = f"Trabajo {trabajo.id_control} creado en estado {trabajo.ruta_proceso.estado.nombre}"
                TrazabilidadTrabajo.objects.registrar_trazabilidad(datos, usuario)
                return Response({'message': f'Trabajo {trabajo.id_control} creado exitosamente'}, status=201)

            return Response(response,  status=200)            
        except CampoRequeridoError as e:
            mensaje = str(e)
            status_code = e.status_code
            return Response({'error': mensaje}, status=status_code)

class ActualizarTrabajo(UpdateAPIView):
    def put(self, request, pk):
        usuario = ValidateUser(request)
        pk = self.kwargs.get('pk')

        try:
            response = Trabajo.objects.actualizar_trabajo(request.data, pk)
            trabajo = response["work"]
            if response["work_exist"]:
                dic = request.data
                campos_actualizados = ""
                for campo in dic.keys():
                    campos_actualizados = campos_actualizados +", "+campo
                
                datos = {}
                datos["trabajo"] = trabajo
                datos["comentario_trazabilidad"] = f"Se actualizaron los campos {campos_actualizados} del trabajo {trabajo.id_control}"
                TrazabilidadTrabajo.objects.registrar_trazabilidad(datos, usuario)
                return Response({'message':  datos["comentario_trazabilidad"]}, status=201)
            
            return Response({'message':  "Trabajo no existe"}, status=200)
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

class SiguienteEstado(UpdateAPIView, CambioEstadoTrabajoMixin):
    def put(self, request, pk):
        usuario = ValidateUser(request)

        if usuario:
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
                return Response({'message': "El trabajo se encuentra en su estado máximo"}, status=200)
            

            arreglo_siguiente_paso = [item for item in ruta_arreglo if item["paso"] == str(paso_siguiente)] # Código del siguiente paso 
            estado_siguiente = arreglo_siguiente_paso[0]["estado"] 

            validacion = self.validar_cambio_estado(paso_siguiente, estado_actual, estado_siguiente, pk)

            if validacion["paso_validado"]:
                response = self.pasar_siguiente_estado(trabajo, paso_siguiente, pk, usuario)
                return Response(response)
            
            return Response(validacion, status=200)
        
        return usuario
       
class AnteriorEstado(UpdateAPIView, CambioEstadoTrabajoMixin):
    def put(self, request, pk):
        usuario = ValidateUser(request)

        if usuario:
            pk = self.kwargs.get('pk')
            comentario_devolucion = request.data["comentario_devolucion"]
            trabajo = Trabajo.objects.get(id_control=pk)
            ruta = RutaProceso.objects.filter(proceso=trabajo.proceso)
            ruta_arreglo=[
                {
                    'paso':r.paso,
                    'estado':r.estado.id_estado,
                }
                for r in ruta]

            paso_actual = trabajo.ruta_proceso.paso
            estado_actual=trabajo.ruta_proceso.estado
            paso_siguiente=int(paso_actual)-1

            if 1 > paso_siguiente:
                return Response({'message':  "El trabajo se encuentra en su estado mínimo"}, status=200)

            arreglo_siguiente_paso=[item for item in ruta_arreglo if item["paso"]==str(paso_siguiente)]
            estado_siguiente=arreglo_siguiente_paso[0]["estado"]

            validacion = self.validar_cambio_estado(paso_siguiente, estado_actual, estado_siguiente, pk)

            if validacion["paso_validado"]:
                response = self.pasar_anerior_estado(trabajo, paso_siguiente, pk, usuario, comentario_devolucion)
                return Response(response)
          
            return Response(validacion, status=200)
        
        return usuario
           
class ObtenerTrabajo(RetrieveAPIView):
    serializer_class = TrabajoSerializer
    def get_queryset(self): 
        usuario = ValidateUser(self.request)

        if usuario:
            pk = self.kwargs.get('pk')
            queryset = Trabajo.objects.filter(id_control=pk)
            return queryset
        
        return usuario

class ContarTrabajosPorProcesos(APIView):
    def get(self,request):
        user = ValidateUser(request)
        if user:    
            vp1 = self.request.query_params.get('vp','')
            ve1 = self.request.query_params.get('ve','')
            kword = self.request.query_params.get('kw','')
            vect_procesos = vp1.split(',')
            vect_estados = ve1.split(',')

            # Lógica para contar trabajo por proceso (Pensar en dejar esta función estática de forma que solo sea consultar)
            response = Trabajo.objects.filtrar_trabajos(vect_procesos, vect_estados, kword, user)
            serializer = TrabajoSerializer(response, many=True)
            procesos = [proceso['proceso'] for proceso in serializer.data]
            nombre_procesos = [proc['nombre'] for proc in procesos]
            conteo_nombre_procesos = Counter(nombre_procesos)
            return Response(conteo_nombre_procesos, status=200)
        
        return user

class ContarTrabajosPorEstado(APIView):
     def get(self,request):
        user = ValidateUser(request)
        if user:
            vp1 = self.request.query_params.get('vp','')
            ve1 = self.request.query_params.get('ve','')
            kword = self.request.query_params.get('kw','')
            vect_procesos = vp1.split(',')
            vect_estados = ve1.split(',')

            # Logica para contar los procesos (Pensar en dejar esto en un botón)
            response = Trabajo.objects.filtrar_trabajos(vect_procesos, vect_estados, kword, user)
            serializer = TrabajoSerializer(response,many=True)
            ruta = [rut['ruta_proceso'] for rut in serializer.data]
            estados = [est['estado'] for est in ruta]
            id_estados = [est['id_estado'] for est in estados]
            conteo_id_estado = Counter(id_estados)
            return Response(conteo_id_estado, status=200)
        
        return user

class SubirArchivoView(APIView):
    def post(self, request, *args, **kwargs):
        user = ValidateUser(request)

        if user:
            data = request.data
            id_trabajo = data['trabajo']
            data['trabajo'] = Trabajo.objects.get(pk=id_trabajo)
            serializer = CrearSoportesInciales(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return user
    
class EliminarSoporteInicial(DestroyAPIView):
    def post(self, request):
        usuario = ValidateUser(request)
        if usuario:
            queryset=SoportesIniciales.objects.all()
            serializer_class = CrearSoportesInciales
            lookup_field='pk'

        return usuario

    def perform_destroy(self, instance):
        if bool(instance.archivo):
            ruta_archivo=os.path.join(settings.MEDIA_ROOT, str(instance.archivo))
            if os.path.exists(ruta_archivo):
                directorio=os.path.dirname(ruta_archivo)
                os.remove(ruta_archivo)
                os.rmdir(directorio)
        
        instance.delete()

class ListarSoportesIniciales(ListAPIView):
    serializer_class=SoportesIncialesSerializer
    def get_queryset(self):
        if usuario:
            usuario = ValidateUser(self.request)
            id_control = self.kwargs.get('pk')
            response=SoportesIniciales.objects.filter(trabajo__id_control=id_control).all()
            return response
        
        return usuario

        