from rest_framework import generics
from rest_framework.views import APIView
from ..users.models import User
from collections import Counter
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt, json
from ..static_data.serializers.unidad_territorial_serializer import UnidadTerritorialSerializer, UnidadTerritorial
from .serializers import (
    PdlTqiSerializer,
    AsignacionesSerializer,
    MetasTQISerializer,
    MetasInspectoresSerializer,
    PdlTqiPagination,
    ManiobraSerializer
)

from .models import(
    PdlTqi,
    Asignaciones,
    MetasTQI,
    MetasInspectores,
    Maniobras,
)

from django.utils import timezone

from django.utils.dateparse import parse_date, parse_time


from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist

import requests, datetime

from ..users.views import ValidateUser

class ListarPdlTqi(generics.ListAPIView):
    serializer_class = PdlTqiSerializer
    # pagination_class = PdlTqiPagination
    def get_queryset(self):
        token = self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, 'secret', algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        # vp1           = self.request.query_params.get('vp' , '')
        # ve1           = self.request.query_params.get('ve' , '')
        # kword         = self.request.query_params.get('kw' , '')
        # vect_procesos = vp1.split( ',' )
        # vect_estados  = ve1.split( ',' )
        
        # response = PdlTqi.objects.filtrar_trabajos( vect_procesos, vect_estados, kword )
        response = PdlTqi.objects.all()
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

class ListarInspectoresPorUnidadesTerritoriales(generics.ListAPIView):
    serializer_class = MetasInspectoresSerializer
    def get_queryset(self):
        token = self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload = jwt.decode(token, 'secret', algorithms = ['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        usuario=User.objects.get(username=payload['username'])

        print(payload['username'])

        if usuario.lider_hse:
            response = MetasInspectores.objects.all()
            for inspector in response:
                inspector.inspector = User.objects.get(username=inspector.inspector)   
        else:
            print("Al menos entra aquí?")
            response = MetasInspectores.objects.filter(inspector=payload['username']).all()
            for inspector in response:
                inspector.inspector = User.objects.get(username=inspector.inspector)  
            
        
        # vp1           = self.request.query_params.get('vp' , '')
        # ve1           = self.request.query_params.get('ve' , '')
        # kword         = self.request.query_params.get('kw' , '')
        # vect_procesos = vp1.split( ',' )
        # vect_estados  = ve1.split( ',' )
        
        # response = PdlTqi.objects.filtrar_trabajos( vect_procesos, vect_estados, kword )
        # response = MetasInspectores.objects.all()
        # for inspector in response:
        #     inspector.inspector = User.objects.get(username=inspector.inspector)
            
        return response

class ActualizacionDatosManiobrasTQI(APIView):
    def post(self, request, *args, **kwargs):
        # token = request.COOKIES.get('jwt')
        # usuario = ValidateUser(self.request)

        # fecha_inicio = '2024-01-20'
        # fecha_fin = '2024-01-31'
        
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
        
        print(lista_respuesta)

        maniobras_aprobadas = [maniobra for maniobra in lista_respuesta if maniobra['estado'] == 'Aprobado' or maniobra['estado'] == 'En ejecución']

        # Update 8:00 pm y 8:00 am
        # 

        for maniobra in maniobras_aprobadas:
            print(maniobra['codigo'])

            try:
                Maniobras.objects.get(codigo = maniobra['codigo'])
                print("Actualizar")
            except ObjectDoesNotExist:
                print("Agregando")

                maniobra["fecha_trabajo_inicio"] = datetime.datetime.strptime(maniobra["fecha_trabajo_inicio"], '%Y-%m-%d').date()
                maniobra["hora_trabajo_inicio"] = datetime.datetime.strptime(maniobra["hora_trabajo_inicio"], '%H:%M:%S').time()
                maniobra["fecha_trabajo_fin"] = datetime.datetime.strptime(maniobra["fecha_trabajo_fin"], '%Y-%m-%d').date()
                maniobra["hora_trabajo_fin"] = datetime.datetime.strptime(maniobra["hora_trabajo_fin"], '%H:%M:%S').time()
                maniobra["fecha_programacion"] = datetime.datetime.strptime(maniobra["fecha_programacion"], '%Y-%m-%d').date()
                maniobra["fecha_actualizacion"] = timezone.now()



                print(type(maniobra["fecha_actualizacion"]))
                serializando = ManiobraSerializer(data=maniobra)
                if serializando.is_valid():
                    print("QQQQQQQQQQQQQ")
                    serializando.save()

                else:
                    print("errores", serializando.errors)
                
        # print(lista_respuesta)

        return Response(maniobras_aprobadas)


        # return Response({'token': "Hola mundo"})

class ObtenerManiobra(generics.RetrieveAPIView):
    serializer_class = PdlTqiSerializer

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
        queryset = PdlTqi.objects.filter(codigo=pk)
        return queryset

class AsignarInspeccion(generics.CreateAPIView):
    serializer_class = AsignacionesSerializer
    def post(self, request):
        token=request.COOKIES.get( 'jwt' )
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        usuario=User.objects.get(username=payload['username'])

        datos_asignacion = {}

        datos_asignacion["pdl_tqi"] = request.data["pdl_tqi"]
        datos_asignacion["cedula_inspector"] = request.data["cedula_inspector"]

        print(datos_asignacion)
        print(datos_asignacion["pdl_tqi"])

        datos_asignacion["cedula_responsable_asignacion"] = usuario.username
        datos_asignacion["fecha_asignacion"] = timezone.now()
        datos_asignacion["ejecutado"] = False

        man = PdlTqi.objects.filter(codigo=datos_asignacion["pdl_tqi"]).first()

        datos_asignacion["estado_stweb"] = man.estado_stweb

        print(man)

        if man.estado_tqi == "2":
            return Response({ "mesage":"Maniobra ya está asignada" })

        serializer = AsignacionesSerializer(data=datos_asignacion)

        if serializer.is_valid():
            man.estado_tqi = 2
            man.save()
            serializer.save()

        # Cambiar el estado de la maniobra a 2

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




            # pdl_tqi
            # cedula_inspector
            # estado_stweb
            # cedula_responsable_asignacion
            # fecha_asignacion
            # ejecutado
        
        # try:
        #     response=Trabajo.objects.crear_trabajo(request.data)
        #     datos={}
        #     datos["trabajo"]=response.id_control
        #     datos["comentario_trazabilidad"]=f"Trabajo {response.id_control} creado en estado {response.ruta_proceso.estado.nombre}"
        #     Trazabilidad.objects.registrar_trazabilidad(datos, usuario)
        #     return Response({'message': f'Trabajo {response.id_control} creado exitosamente'}, status=201)
        # except CampoRequeridoError as e:
        #     mensaje = str(e)
        #     status_code = e.status_code
        #     return Response({'error': mensaje}, status=status_code)

class EliminarUnaAsignacion(APIView):
    def delete(self, request, *args, **kwargs):
        usuario = ValidateUser(request)

        maniobra = kwargs.get('pk')
        asignacion = Asignaciones.objects.filter(pdl_tqi=maniobra)
        asignacion.delete()

        maniobra = PdlTqi.objects.filter(codigo=maniobra).first()
        maniobra.estado_tqi = 0
        maniobra.save()

        return Response({ "mesaage": "Asignación eliminada" })

class CreateManiobraTqi(APIView):
    def post(self, request, *args, **kwargs):
        usuario = ValidateUser(request)

        datos = request.data

        print(datos)

        serializar = PdlTqiSerializer(data=datos)

        if serializar.is_valid():
            serializar.save()
            return Response({ "Mesagge": "Masniobra creada" })
        else:
            return Response({"Error": serializar.errors})