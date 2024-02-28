from rest_framework.response import Response
from ..lcl_management.models import Lcl
from ..budgets_management.models import Valorizacion
from ..odm_management.models import Odm
from ..scheduling_management.models import Programacion
from .models import Trabajo
from ..static_data.models.ruta_proceso import RutaProceso
from ..traceability_management.models import TrazabilidadTrabajo
from .errores import CampoRequeridoError, NoTienSiguienteEstado

class CambioEstadoTrabajoMixin(object):

    def validar_cambio_estado(paso_maximo, paso_siguiente, estado_actual, estado_siguiente, pk):

        if estado_actual.id_estado == "E02" and estado_siguiente == "E03":
            valorizaciones = Valorizacion.objects.filter(trabajo__id_control=pk).all()
            if not valorizaciones.exists():
                return Response({'message':  "El trabajo no tiene valorizaciones cargadas"}, status=205)
            
        if estado_actual.id_estado == "E03" and estado_siguiente == "E04":
            valorizaciones = Valorizacion.objects.filter(trabajo__id_control=pk).all()
            estado_valorizaciones = [val.estado for val in valorizaciones]
            if not valorizaciones.exists() or all(valor == "0" for valor in estado_valorizaciones):
                return Response({'message': "El trabajo no tiene valorizaciones aprobada"}, status=205)
            
        if estado_actual.id_estado=="E04" and estado_siguiente=="E05":
            odms = Odm.objects.obtener_odms(pk)
            if not odms.exists():
                return Response({'message':  "El trabajo no tiene odms activas"}, status=205)

        if estado_actual.id_estado=="E05" and estado_siguiente=="E06":
            lcls = Lcl.objects.obtener_lcls(pk)
            arr_lcl=[lcl.estado_lcl for lcl in lcls]
            if not lcls.exists() or any(valor!="0" for valor in arr_lcl):
                return Response({'message':  "El trabajo no tiene lcls activas en liberación operativa"}, status=205)

        if estado_actual.id_estado=="E06" and estado_siguiente=="E07":
            lcls = Lcl.objects.obtener_lcls(pk)
            arr_lcl=[lcl.estado_lcl for lcl in lcls]
            if not lcls.exists() or not any(valor=="1" for valor in arr_lcl):
                return Response({'message':  "El trabajo debe tener almenos una LCL liberada"}, status=205)
            
        if estado_actual.id_estado=="E07" and estado_siguiente=="E08":
            lcls = Lcl.objects.obtener_lcls(pk)
            arr_lcl=[lcl.estado_lcl for lcl in lcls]
            if not lcls.exists() or not any(valor=="2" for valor in arr_lcl):
                return Response({'message':  "El trabajo debe tener almenos una LCL en SCM"}, status=205)
            
        if estado_actual.id_estado=="E08" and estado_siguiente=="E09":
            lcls=Lcl.objects.obtener_lcls(pk)
            arr_lcl=[lcl.estado_lcl for lcl in lcls]
            if not lcls.exists() or not any(valor=="2" for valor in arr_lcl):
                return Response({'message':  "El trabajo debe tener almenos una LCL en SCM"}, status=205)
        
        if estado_actual.id_estado == "E09" and estado_siguiente == "E10":
            programacion = Programacion.objects.filter(trabajo__id_control=pk).all()
            if not programacion.exists():
                return Response({'message': "El trabajo no tiene una programación para agreagar una maniobra"}, status=205)
        
        if estado_actual.id_estado=="E03" and estado_siguiente=="E02":
            valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
            ser_val=[val.estado for val in valorizaciones]
            if all(valor !="1" for valor in ser_val):
                return Response({'message':  "El trabajo no tiene valorizaciones rechazadas"}, status=205)
            
        if estado_actual.id_estado=="E04" and estado_siguiente=="E03":
            valorizaciones=Valorizacion.objects.filter(trabajo__id_control=pk).all()
            ser_val=[val.estado for val in valorizaciones]
            if any(valor !="1" for valor in ser_val):
                return Response({'message':  "El trabajo no tiene valorizaciones rechazada"}, status=205)

        if estado_actual.id_estado=="E05" and estado_siguiente=="E04":
            odms=Odm.objects.obtener_odms(pk)
            if odms.exists():
                return Response({'message':  "El trabajo tiene odms activas"}, status=205)

        if estado_actual.id_estado=="E06" and estado_siguiente=="E05":
            lcls=Lcl.objects.obtener_lcls(pk)
            if lcls.exists() :
                return Response({'message':  "El trabajo tiene lcls activas"}, status=205)
        
        if 1 > paso_siguiente:
            return Response({'message': "El trabajo no tiene un estado anterior"}, status=205)

    def pasar_siguiente_estado(self, trabajo, paso_siguiente, pk, usuario):
        try:
            datos_actualizacion = {"ruta_proceso":RutaProceso.objects.get(proceso=trabajo.proceso, paso=paso_siguiente)}
            response = Trabajo.objects.actualizar_trabajo(datos_actualizacion, pk)
            campos_actualizados = datos_actualizacion['ruta_proceso']
            
            datos = {}
            datos["trabajo"] = response.id_control
            datos["comentario_trazabilidad"] = f"Se cambiado al estado del trabajo {response.id_control} a {campos_actualizados.estado.nombre}"
            TrazabilidadTrabajo.objects.registrar_trazabilidad(datos, usuario)
            return Response({'message':  datos["comentario_trazabilidad"]}, status=201)
        except CampoRequeridoError as e:
            mensaje = str(e)
            status_code = e.status_code
            return Response({'error': mensaje}, status=status_code)
        except NoTienSiguienteEstado as e:
            mensaje = str(e)
            status_code = e.status_code
            return Response({'error': mensaje}, status=status_code)
    
    def pasar_anerior_estado(self, trabajo, paso_siguiente, pk, usuario, comentario_devolucion):
        try:
            datos_actualizacion={"ruta_proceso":RutaProceso.objects.get(proceso=trabajo.proceso, paso=paso_siguiente)}
            response=Trabajo.objects.actualizar_trabajo(datos_actualizacion, pk)
            campos_actualizados=datos_actualizacion['ruta_proceso']
            
            datos = {}
            datos["trabajo"] = response.id_control
            datos["comentario_trazabilidad"]=f"Se cambiado al estado del trabajo {response.id_control} a {campos_actualizados.estado.nombre}, con el comentario { comentario_devolucion }"

            TrazabilidadTrabajo.objects.registrar_trazabilidad(datos, usuario)
            return Response({'message':  datos["comentario_trazabilidad"]}, status=201)
        except CampoRequeridoError as e:
            mensaje = str(e)
            status_code = e.status_code
            return Response({'error': mensaje}, status=status_code)
        except NoTienSiguienteEstado as e:
            mensaje = str(e)
            status_code = e.status_code
            return Response({'error': mensaje}, status=status_code)