from rest_framework.generics import (
    CreateAPIView, 
    DestroyAPIView,
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


class CrearTrabajoView(CreateAPIView):
    serializer_class = CrearTrabajoSerializer
    def post(self, request):        
        usuario = ValidateUser(request)

        if usuario["valid_user"]:

            try:
                response = Trabajo.objects.crear_trabajo(request.data)

                if response["creado_exitosamente"]:

                    datos = {}
                    trabajo = response["trabajo"]
                    datos["trabajo"] = trabajo
                    datos["comentario_trazabilidad"] = f"Trabajo {trabajo.id_control} creado en estado {trabajo.ruta_proceso.estado.nombre}"
                    TrazabilidadTrabajo.objects.registrar_trazabilidad(datos, usuario["user"])
                    return Response({'message': f'Trabajo {trabajo.id_control} creado exitosamente'}, status=201)

                return Response(response,  status=200)            
            except CampoRequeridoError as e:
                mensaje = str(e)
                status_code = e.status_code
                return Response({'error': mensaje}, status=status_code)
        
        return usuario


class ListarTrabajosView(APIView):
    def get(self, request):
        user = ValidateUser(request)

        if user["valid_user"]:
            vp1 = self.request.query_params.get('vp', '')
            ve1 = self.request.query_params.get('ve', '')
            kword = self.request.query_params.get('kw', '')
            vect_procesos = vp1.split(',')
            vect_estados  = ve1.split(',')
        
            response = Trabajo.objects.filtrar_trabajos(vect_procesos, vect_estados, kword, user["user"])
            serializer = TrabajoSerializer(response, many=True)

            return Response(serializer.data)
        
        return Response(user)


class ObtenerDetalleTrabajoView(APIView):
    def get(self, request, *args, **kwargs): 
        usuario = ValidateUser(request)

        if usuario["valid_user"]:
            pk = self.kwargs.get('pk')
            trabajo = Trabajo.objects.obtener_detalle_trabajo(pk)
            serializer = TrabajoSerializer(trabajo, many=True)
            return Response(serializer.data)
        
        return Response(usuario)


class ActualizarTrabajoView(APIView):
    def put(self, request, *args, **kwargs):
        usuario = ValidateUser(request)
        pk = self.kwargs.get('pk')

        if usuario["valid_user"]:
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
                    TrazabilidadTrabajo.objects.registrar_trazabilidad(datos, usuario["user"])
                    return Response({'message':  datos["comentario_trazabilidad"]}, status=201)
                
                return Response({'message':  "Trabajo no existe"}, status=200)
            except CampoRequeridoError as e:
                mensaje = str(e)
                status_code = e.status_code
                return Response({'error': mensaje}, status=status_code)
        
        return Response(usuario)


class EliminarTrabajoView(DestroyAPIView):
    def post(self, request):
        usuario = ValidateUser(request)
        
        queryset = Trabajo.objects.all()
        serializer_class = TrabajoSerializer
        lookup_field = 'pk'


class SiguienteEstadoView(APIView, CambioEstadoTrabajoMixin):
    def put(self, request, *args, **kwargs):
        usuario = ValidateUser(request)

        if usuario["valid_user"]:
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
                response = self.pasar_siguiente_estado(trabajo, paso_siguiente, pk, usuario["user"])
                return Response(response)
            
            return Response(validacion, status=200)
        
        return Response(usuario)
       

class AnteriorEstadoView(APIView, CambioEstadoTrabajoMixin):
    def put(self, request, *args, **kwargs):
        usuario = ValidateUser(request)

        if usuario["valid_user"]:
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
                response = self.pasar_anerior_estado(trabajo, paso_siguiente, pk, usuario["user"], comentario_devolucion)
                return Response(response)
          
            return Response(validacion, status=200)
        
        return Response(usuario)
           

class ContarTrabajosPorProcesosView(APIView):
    def get(self, request):
        user = ValidateUser(request)
        if user["valid_user"]:    
            vp1 = self.request.query_params.get('vp','')
            ve1 = self.request.query_params.get('ve','')
            kword = self.request.query_params.get('kw','')
            vect_procesos = vp1.split(',')
            vect_estados = ve1.split(',')

            response = Trabajo.objects.filtrar_trabajos(vect_procesos, vect_estados, kword, user["user"])
            serializer = TrabajoSerializer(response, many=True)
            procesos = [proceso['proceso'] for proceso in serializer.data]
            nombre_procesos = [proc['nombre'] for proc in procesos]
            conteo_nombre_procesos = Counter(nombre_procesos)
            return Response(conteo_nombre_procesos, status=200)
        
        return Response(user)


class ContarTrabajosPorEstadoView(APIView):
     def get(self,request):
        user = ValidateUser(request)
        if user["valid_user"]:
            vp1 = self.request.query_params.get('vp','')
            ve1 = self.request.query_params.get('ve','')
            kword = self.request.query_params.get('kw','')
            vect_procesos = vp1.split(',')
            vect_estados = ve1.split(',')

            # Logica para contar los procesos (Pensar en dejar esto en un botón)
            response = Trabajo.objects.filtrar_trabajos(vect_procesos, vect_estados, kword, user["user"])
            serializer = TrabajoSerializer(response,many=True)
            ruta = [rut['ruta_proceso'] for rut in serializer.data]
            estados = [est['estado'] for est in ruta]
            id_estados = [est['id_estado'] for est in estados]
            conteo_id_estado = Counter(id_estados)
            return Response(conteo_id_estado, status=200)
        
        return Response(user)


class SubirArchivoView(APIView):
    def post(self, request, *args, **kwargs):
        user = ValidateUser(request)

        if user["valid_user"]:
            data = request.data
            id_trabajo = data['trabajo']
            data['trabajo'] = Trabajo.objects.get(pk=id_trabajo)
            serializer = CrearSoportesInciales(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        return Response(user)


class EliminarSoporteInicialView(APIView):
    def delete(self, request, *args, **kwargs):
        usuario = ValidateUser(request)
        if usuario["valid_user"]:
            id_soporte = self.kwargs.get('pk')
            file = SoportesIniciales.objects.filter(id_soporte=id_soporte).first()

            if file:
                if bool(file.archivo):
                    ruta_archivo = os.path.join(settings.MEDIA_ROOT, str(file.archivo))
                    if os.path.exists(ruta_archivo):
                        directorio=os.path.dirname(ruta_archivo)
                        os.remove(ruta_archivo)
                        os.rmdir(directorio)
                file.delete()
                return Response({"message":f"Archivo {id_soporte} eliminado."}, status=200)
            
            return Response({"message":"Nada que eliminar" }, status=200)

        return Response(usuario)


class ListarSoportesInicialesView(APIView):
    def get(self, request, *args, **kwargs):
        usuario = ValidateUser(request)
        if usuario["valid_user"]:
            id_control = self.kwargs.get('pk')
            archivos = SoportesIniciales.objects.filter(trabajo__id_control=id_control).all()
            serializer = SoportesIncialesSerializer(archivos, many=True)
            return Response(serializer.data)
        
        return Response(usuario)

        