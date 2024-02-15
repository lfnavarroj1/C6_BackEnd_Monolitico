from rest_framework import generics
from rest_framework.views import APIView
from ..users.models import User
from collections import Counter
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, json
from ..static_data.serializers.unidad_territorial_serializer import UnidadTerritorialSerializer, UnidadTerritorial
from .serializers import (
    ManiobrasTqiSerializer,
    MetasTQISerializer,
    MetasInspectoresSerializer,
    PdlTqiPagination,
    MetasInspectoresTotalesSerializer,
    MetasTQIContratoSerializer,
)

from ..users.serializers import UserSerializer

from .models import(
    ManiobrasTqi,
    MetasTQI,
    MetasInspectores,

)

from ..static_data.models.municipio import Municipio
from ..static_data.models.circuito import Circuito
from ..static_data.models.subestacion import Subestacion
from ..static_data.models.unidad_territorial import UnidadTerritorial
from ..static_data.models.contrato import Contrato


from django.utils import timezone

from django.utils.dateparse import parse_date, parse_time


from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist

import requests, datetime

from ..users.views import ValidateUser

from django.db.models import Sum

class ListarPdlTqi(generics.ListAPIView):
    serializer_class = ManiobrasTqiSerializer
    # pagination_class = PdlTqiPagination
    def get_queryset(self):
        token = self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, 'secret', algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        vector_uno = self.request.query_params.get('vector_unidades_territoriales' , '')
        vector_dos = self.request.query_params.get('vector_contratos' , '')
        vector_tres = self.request.query_params.get('vector_estados' , '')
        vector_cuatro = self.request.query_params.get('vector_anio' , '')
        vector_cinco = self.request.query_params.get('vector_mes' , '')

        vector_unidades_territoriales = vector_uno.split( ',' )
        vector_contratos = vector_dos.split( ',' )
        vector_estados = vector_tres.split( ',' )
        vector_anio = vector_cuatro.split( ',' )
        vector_meses = vector_cinco.split( ',' )
        kword = self.request.query_params.get('kw' , '')
        
        print(vector_unidades_territoriales)
        
        response = ManiobrasTqi.objects.filtrar_maniobras( vector_unidades_territoriales, vector_contratos, vector_estados, vector_anio, vector_meses, kword )
        # response = ManiobrasTqi.objects.all()
        return response

class ListarContratosPorUnidadesTerritoriales(generics.ListAPIView):
    serializer_class = UnidadTerritorialSerializer
    def get_queryset(self):

        token = self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, 'secret', algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        response = UnidadTerritorial.objects.all()
        return response

class ListarInspectores(generics.ListAPIView):
    serializer_class = MetasInspectoresTotalesSerializer
    def get_queryset(self):
        usuario=ValidateUser(self.request)

        vector_cuatro = self.request.query_params.get('vector_anio' , '')
        vector_cinco = self.request.query_params.get('vector_mes' , '')

        vector_anio = vector_cuatro.split( ',' )
        vector_meses = vector_cinco.split( ',' )

        if usuario.lider_hse:
            # response = MetasInspectores.objects.filtrar_inspectores(vector_anio, vector_meses)
            # response = MetasInspectores.objects.values('inspector').annotate(total_meta=Sum('cantidad_meta'), total_programada=Sum('cantidad_programada'), total_ejecutada=Sum('cantidad_ejecutada')).filter(anio__in = vector_anio, mes__in = vector_meses)
            if vector_anio and vector_meses:
                # Si ambos vectores tienen elementos, realiza la consulta normalmente
                response = MetasInspectores.objects.values('inspector').annotate(
                    total_meta=Sum('cantidad_meta'),
                    total_programada=Sum('cantidad_programada'),
                    total_ejecutada=Sum('cantidad_ejecutada')
                ).filter(
                    anio__in=vector_anio,
                    mes__in=vector_meses
                )
            else:
                # Si alguno de los vectores está vacío, asigna un arreglo vacío a la variable response
                response = []
            
            for elemento in response:
                inspector_id = elemento['inspector']
                inspector = User.objects.get(username=inspector_id)
                elemento['inspector'] = inspector

        else:
            print("Al menos entra aquí?")
            response = MetasInspectores.objects.filter(inspector=usuario).all()
            for inspector in response:
                inspector.inspector = User.objects.get(username=inspector.inspector)  
            
        return response

class ListarInspectoresParaAsignacion(generics.ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        usuario=ValidateUser(self.request)

        pk = self.kwargs.get('pk')
        datos_maniobra = ManiobrasTqi.objects.filter(codigo=pk).first()

        inspectores = MetasInspectores.objects.filter(anio=datos_maniobra.anio, mes=datos_maniobra.mes).all()
        response = [inspector.inspector for inspector in inspectores if datos_maniobra.unidad_ejecutora in inspector.inspector.unidades_territoriales.all()]
            
        return response

class ActualizacionDatosManiobrasTQI(APIView):
    def post(self, request, *args, **kwargs):
        usuario = ValidateUser(self.request)
        
        fecha_inicio = timezone.now().date()
        fecha_fin = fecha_inicio + datetime.timedelta(days=30)

        url_api_pms = 'http://143.198.142.162/api-jwt/auth/'
        url_api_list = 'http://143.198.142.162/gds/api/v2/STWeb-TQI/?format=json&start_date={}&end_date={}'.format(fecha_inicio, fecha_fin)
        body_api = {
            "username": "PM-STQI",
            "password": "G4_JlV0BcYpRZ9w0Q"  
        }

        response = requests.post(url_api_pms, data=body_api)
        token_api = response.json().get('token', '')
        header = {'Authorization': 'jwt {}'.format(token_api)}

        listado_maniobras = requests.get(
            url_api_list,
            headers = header
        )

        lista_respuesta = listado_maniobras.json()
        maniobras_aprobadas = [maniobra for maniobra in lista_respuesta if maniobra['estado'] == 'Aprobado' or maniobra['estado'] == 'En ejecución']


        for maniobra in maniobras_aprobadas:
            try:
                ManiobrasTqi.objects.get(codigo = maniobra['codigo'])
                print("Actualizar {}".format(maniobra['codigo']))
            except ObjectDoesNotExist:
                nueva_maniobra = {}
                nueva_maniobra["codigo"] = maniobra["codigo"]

                tipo_maniobra = ManiobrasTqi.obtener_valor_tipo_maniobra(maniobra["tipo"])
                if tipo_maniobra:
                    nueva_maniobra["tipo"] = tipo_maniobra
                else:
                     nueva_maniobra["tipo"] = ""

                nueva_maniobra["descripcion"] = maniobra["descripcion"]
                estado_maniobra =  ManiobrasTqi.obtener_valor_estado_stweb(maniobra["estado"])
                if estado_maniobra:
                   nueva_maniobra["estado_stweb"] = estado_maniobra
                else:
                    nueva_maniobra["estado_stweb"] = ""

                nueva_maniobra["fecha_inicio"] = datetime.datetime.strptime(maniobra["fecha_trabajo_inicio"], '%Y-%m-%d').date()
                nueva_maniobra["hora_inicio"] = datetime.datetime.strptime(maniobra["hora_trabajo_inicio"], '%H:%M:%S').time()
                nueva_maniobra["fecha_fin"] = datetime.datetime.strptime(maniobra["fecha_trabajo_fin"], '%Y-%m-%d').date()
                nueva_maniobra["hora_fin"] = datetime.datetime.strptime(maniobra["hora_trabajo_fin"], '%H:%M:%S').time()
                nueva_maniobra["pdl_asociado"] = maniobra["pdl_asociado"]
                nueva_maniobra["fecha_actualizacion"] = timezone.now()                
                nueva_maniobra["direccion"] = maniobra["ubicacion"]

                cadena = maniobra["circuito"]

                indice_corchete_abierto = cadena.find('[')
                if indice_corchete_abierto != -1:
                    indice_espacio_anterior_corchete = cadena.rfind(' ', 0, indice_corchete_abierto)

                    if indice_espacio_anterior_corchete + 1 == indice_corchete_abierto:
                        indice_espacio_anterior_corchete = 0

                    if indice_corchete_abierto != -1 and indice_espacio_anterior_corchete != -1:
                        resultado = cadena[indice_espacio_anterior_corchete:indice_corchete_abierto-1]

                circuito = Circuito.objects.filter(nombre__icontains = resultado).first()

                if circuito:
                    nueva_maniobra["circuito"] = circuito.codigo_circuito
                    subestacion = Subestacion.objects.filter(codigo=circuito.subestacion.codigo).first() #cambiar por la del circuito
                    if subestacion:
                        nueva_maniobra["subestacion"] = subestacion.codigo
                        for unit in subestacion.unidades_territoriales.all():
                            unidad_general = unit
                        if unidad_general:
                            nueva_maniobra["unidad_territorial"] = unidad_general.numero
                            nueva_maniobra["unidad_ejecutora"] = unidad_general.numero
                        else:
                            nueva_maniobra["unidad_territorial"] = ""
                            nueva_maniobra["unidad_ejecutora"] = ""

                    else:
                        nueva_maniobra["subestacion"] = ""
                else:
                    nueva_maniobra["circuito"] = ""
                    nueva_maniobra["subestacion"] = ""
                    nueva_maniobra["unidad_territorial"] = ""
                    nueva_maniobra["unidad_ejecutora"] = ""

                tipo_causa = ManiobrasTqi.obtener_valor_tipo_causa(maniobra["causal"])
                if tipo_causa:
                     nueva_maniobra["causal"] = tipo_causa
                else:
                     nueva_maniobra["tipo"] = ""

                nueva_maniobra["estado_tqi"] = "0"
                nueva_maniobra["criticidad_maniobra"] = ""
                nueva_maniobra["cuadrilla_responsable"] = maniobra["nombre_responsable"]
                nueva_maniobra["telefono_cuadrilla_responsable"] = maniobra["telefono_reponsable"]
                # nueva_maniobra["inspector_asingado"] = ""

                unidad_entera = maniobra["unidad_responsable"]
                unidad_opcion = unidad_entera[0:4]

                contrato_maniobra = Contrato.objects.filter(nombre__icontains=unidad_opcion, gestoria =  nueva_maniobra["unidad_territorial"]).first()

                if contrato_maniobra:
                    nueva_maniobra["contrato"] = contrato_maniobra.numero_contrato
                else:
                     nueva_maniobra["contrato"] = ""


                # nueva_maniobra["contrato"] = ""

                nueva_maniobra["municipio"] = ""
                nueva_maniobra["vereda_localidad"] = ""

                serializando = ManiobrasTqiSerializer(data=nueva_maniobra)
                if serializando.is_valid():
                    serializando.save()
                else:
                    print("errores", serializando.errors)

        return Response(maniobras_aprobadas)

class ObtenerManiobra(generics.RetrieveAPIView):
    serializer_class = ManiobrasTqiSerializer
    def get_queryset(self):
        usuario = ValidateUser(self.request)
        pk = self.kwargs.get('pk')

        queryset = ManiobrasTqi.objects.filter(codigo=pk)
        return queryset

class AsignarInspeccion(generics.CreateAPIView):
    serializer_class = ManiobrasTqiSerializer
    def post(self, request):
        usuario = ValidateUser(request)

        print(request.data)

        maniobra_actualizar = ManiobrasTqi.objects.filter(codigo = request.data["codigo"]).first()

        if maniobra_actualizar:
            if maniobra_actualizar.estado_tqi == "2":
                return Response({ "mesage":"Maniobra ya está asignada" })
            else:
                maniobra_actualizar.inspector_asingado =  User.objects.filter(username=request.data["cedula_inspector"]).first()
                maniobra_actualizar.estado_tqi = 2
                maniobra_actualizar.save()

                ajuste_programacion = MetasInspectores.objects.filter(inspector=maniobra_actualizar.inspector_asingado, anio=maniobra_actualizar.anio, mes=maniobra_actualizar.mes).first()
                print(ajuste_programacion)
                ajuste_programacion.cantidad_programada = ajuste_programacion.cantidad_programada + 1
                ajuste_programacion.save()

                return Response({ "mesage":"Maniobra asignada" })
        else:
            return Response({ "mesage":"Maniobra no existe" })

class CalcularCantidadesGenerales(APIView):
    def post(self, request, *args, **kwargs):
        # Por cada inspector TQI, contar las cantidades ejecutadas y las cantidades programada
        # por anio y por mes
        inspectores_anio_mes = MetasInspectores.objects.all()
        for caso in inspectores_anio_mes:
            print(caso)

    
        return Response({ "mesage":"Calculos y ajustes realizados" })

class EliminarUnaAsignacion(APIView):
    def delete(self, request, *args, **kwargs):
        usuario = ValidateUser(request)
        pk = self.kwargs.get('pk')

        maniobra_actualizar = ManiobrasTqi.objects.filter(codigo = pk).first()

        if maniobra_actualizar:
            if maniobra_actualizar.estado_tqi !="0":

                print(maniobra_actualizar)
                print(maniobra_actualizar.inspector_asingado)

                ajuste_programacion = MetasInspectores.objects.filter(inspector=maniobra_actualizar.inspector_asingado, anio=maniobra_actualizar.anio, mes=maniobra_actualizar.mes).first()
                print(ajuste_programacion)
                ajuste_programacion.cantidad_programada = ajuste_programacion.cantidad_programada - 1
                ajuste_programacion.save()

                maniobra_actualizar.inspctor_asingado =  ""
                maniobra_actualizar.estado_tqi = 0
                maniobra_actualizar.save()
                return Response({ "mesage":"Asingacion eliminada" })
            else:               
                return Response({"mesage":"Maniobra está sin asignar"})
        else:
            return Response({ "mesage":"Maniobra no existe" })
      
class CreateManiobraTqi(APIView):
    def post(self, request, *args, **kwargs):
        usuario = ValidateUser(request)

        datos = {}
        datos = request.data.copy()

        datos['estado_tqi'] = "0"
        datos['inspector_asingado'] = ""

        serializar = ManiobrasTqiSerializer(data=datos)
        if serializar.is_valid():
            serializar.save()
            return Response({ "Mesagge": "Masniobra creada" })
        else:
            return Response({"Error": serializar.errors})
        

class ObtenerMetasTqi (generics.ListAPIView):
    serializer_class = MetasTQIContratoSerializer
    def get_queryset(self):
        usuario = ValidateUser(self.request)

        vector_dos = self.request.query_params.get('vector_contratos' , '')
        vector_cuatro = self.request.query_params.get('vector_anio' , '')
        vector_cinco = self.request.query_params.get('vector_mes' , '')

        vector_contratos = vector_dos.split( ',' )
        vector_anio = vector_cuatro.split( ',' )
        vector_meses = vector_cinco.split( ',' )

        print(vector_contratos)
        print(vector_anio)
        print(vector_meses)

        if vector_anio and vector_meses and vector_contratos:
            # Si ambos vectores tienen elementos, realiza la consulta normalmente
            response = MetasTQI.objects.values('contrato').annotate(
                total_meta=Sum('cantidad_meta'),
                total_programada=Sum('cantidad_programada'),
                total_ejecutada=Sum('cantidad_ejecutada')
            ).filter(
                contrato__in = vector_contratos,
                anio__in=vector_anio,
                mes__in=vector_meses
            )
        else:
            # Si alguno de los vectores está vacío, asigna un arreglo vacío a la variable response
            response = []
        
        for elemento in response:
            contrato_num = elemento['contrato']
            contrato = Contrato.objects.get(numero_contrato=contrato_num)
            elemento['contrato'] = contrato

        return response