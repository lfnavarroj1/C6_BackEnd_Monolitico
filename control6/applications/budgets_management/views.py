from rest_framework import generics
from rest_framework.generics import (
    ListAPIView,  
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView
)
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (
    Valorizacion, Nodo
)
from .serializers import ( 
    ValorizacionSerializer, 
    NodoSerializer, 
    EtlBudgetSerializer,
    NodoMDOSerializer, 
    NodoMATerializer, 
    CrearNodoRG10Serializer,
    NodoSerializer
)
from ..work_management.models import Trabajo
from rest_framework.exceptions import AuthenticationFailed
import jwt, os
from django.utils import timezone

from django.conf import settings
from .models import ( 
    NodoMAT, 
    NodoMDO, 
    EtlBudget 
)
from ..labour_management.models import Prestacion
from ..materials_management.models import Material
from ..lcl_management.models import Lcl
import pandas as pd
import functools
from itertools import groupby
from django.utils import timezone
from ..users.views import ValidateUser
from .mixins import CargarFormatoReplanteoMixin, EliminarValorizacionMixin

class AgregarValorizacionView(APIView, CargarFormatoReplanteoMixin, EliminarValorizacionMixin):
    def post(self, request, *args, **kwargs):
        usuario =  ValidateUser(request)

        if usuario["valid_user"]:

            data = request.data
            id_trabajo = data['trabajo']
            data['trabajo'] = Trabajo.objects.filter(pk=id_trabajo).first()

            if data["trabajo"]:

                data["fecha_valorizacion"] = timezone.now()

                es_formato_excel = self.validar_formato(data['presupuesto'])
                if not es_formato_excel:
                    return Response ({"message": "El archivo no está en formato Excel", "error_formato":True})
                
                es_formato_rg = self.validar_rg(data['presupuesto'])
                if not es_formato_rg["es_formato_rg"]:
                    return Response ({"message": "El archivo cargado no tiene el formato RG para presupuestos", "error_formato":True})

                serializer = ValorizacionSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response({'message:': serializer.errors}, status=205)
            
                if es_formato_rg["formato"] == "RG10":
                    respuesta = self.cargar_rg10(data['presupuesto'], serializer) 
                elif es_formato_rg["formato"] == "RG11":
                    respuesta = self.cargar_rg11(data['presupuesto'], serializer)
                elif es_formato_rg["formato"] == "RG12":
                    respuesta = self.cargar_rg12(data['presupuesto'], serializer)

                if respuesta['eliminar']:
                    self.eliminarNodos(serializer.data["id_valorizacion"])
                    self.eliminiarValorizacion(serializer.data["id_valorizacion"])

                return Response(respuesta, status=201)
            
            return Response({"mesage":"El trabajo no existe"})
        
        return Response(usuario)


class ListarValorizacionTodoView(ListAPIView):
    serializer_class = ValorizacionSerializer
    def get_queryset(self):
        usuario = ValidateUser(self.request)

        #Se debe tener el vector del contrato, de la unidad encontrados con los unidades y contratos del trabajo

        if usuario:
            id_control = self.kwargs.get('pk') # <-- Toca manejar el error aquí.
            response = Valorizacion.objects.listar_valorizaciones(trabajo__id_control = id_control).all()
            return response
        
        return usuario


class ListarValorizacionTrabajoView(ListAPIView):
    serializer_class = ValorizacionSerializer
    def get_queryset(self):
        usuario = ValidateUser(self.request)

        #Se debe tener el vector del contrato, de la unidad encontrados con los unidades y contratos del trabajo

        if usuario:
            id_control = self.kwargs.get('pk') # <-- Toca manejar el error aquí.
            response = Valorizacion.objects.filter(trabajo__id_control = id_control).all()
            return response
        
        return usuario


class ObtenerDetalleValorizacionView(RetrieveAPIView):
    serializer_class = ValorizacionSerializer

    def get_queryset(self):
        usuario = ValidateUser(self.request)

        if usuario:
            id_valorizacion = self.kwargs.get('pk')
            queryset = Valorizacion.objects.obtener_detalle_trabajo(id_valorizacion)
            return queryset
        
        return usuario


class ActualizarValorizacionView(UpdateAPIView, CargarFormatoReplanteoMixin, EliminarValorizacionMixin):
    def put( self, request, pk ):
        usuario = ValidateUser(request)

        if usuario:
            data = request.data

            es_formato_excel = self.validar_formato(data['presupuesto'])
            if not es_formato_excel:
                return Response ({"message": "El archivo no está en formato Excel", "error_formato":True})
            
            es_formato_rg = self.validar_rg(data['presupuesto']) #< -- Este metodo debe devolver el tipo de rg que se está cargando
            if not es_formato_rg:
                return Response ({"message": "El archivo cargado no tiene el formato RG para presupuestos", "error_formato":True})

            id_valorizacion = self.kwargs.get('pk')

            if "presupuesto" in data:
                self.eliminarNodos(id_valorizacion)
                self.eliminiarValorizacion(id_valorizacion)
            
            
            try:
                valorizacion = Valorizacion.objects.actualizar_valorizacion(request.data, pk)

                if "presupuesto" in request.data:
                    if es_formato_rg["formato"] == "RG10":
                        respuesta = self.cargar_rg10(data['presupuesto'], valorizacion) 
                    elif es_formato_rg["formato"] == "RG11":
                        respuesta = self.cargar_rg11(data['presupuesto'], valorizacion)
                    elif es_formato_rg["formato"] == "RG12":
                        respuesta = self.cargar_rg12(data['presupuesto'], valorizacion)

                    if respuesta['eliminar']:
                        self.eliminarNodos(id_valorizacion)
                        self.eliminiarValorizacion(id_valorizacion)

                return Response(respuesta, status=201)

            except Exception as e:
                mensaje = str(e)
                status_code = 412  
                return Response({'error': mensaje}, status=status_code)
            
        return usuario


class EliminarValorizacionView(DestroyAPIView):
    def put(self, request):
        usuario = ValidateUser(request)
        queryset = Valorizacion.objects.all()
        serializer_class = ValorizacionSerializer
        lookup_field='pk'

    def eliminar_datos_relacionados(self, valorizacion):
        nodos_relacionados = Nodo.objects.filter(valorizacion=valorizacion).all()
        for nodo in nodos_relacionados:
            print(nodo)
            mdos_relacionadas=NodoMDO.objects.filter(nodo=nodo).all()
            for mdo in mdos_relacionadas:
                mdo.delete()
            mats_relacionados=NodoMAT.objects.filter(nodo=nodo).all()
            for mat in mats_relacionados:
                mat.delete()
            nodo.delete()

    def perform_destroy(self, instance):
        self.eliminar_datos_relacionados(instance)
        ruta_archivo=os.path.join(settings.MEDIA_ROOT,str(instance.presupuesto))
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)
        instance.delete()


class CalcularValorizacionView(generics.UpdateAPIView):
    def put (self, request, pk):        
        usuario = ValidateUser(request)
        pk = self.kwargs.get('pk')
        
        try:

            budget_val = EtlBudget.objects.filter(nodo__valorizacion=pk).all()

            
            # Cargar el valor a cada diccionario
            for val in budget_val:


                if Prestacion.objects.filter( codigo_prestacion = val.codigo).first():
                    mdo = {}
                    mdo["nodo"] = val.nodo
                    mdo["tipo_trabajo_mdo"] = val.instalacion_retiro
                    mdo["codigo_mdo"] = val.codigo
                    mdo["cantidad_replanteada"] = val.cantidad

                    serializer_mdo = NodoMDOSerializer(data = mdo)
                    if serializer_mdo.is_valid():
                        serializer_mdo.save()

                elif Material.objects.filter( codigo_material = val.codigo).first():
                    mat = {}
                    mat[ "nodo" ] = val.nodo

                    if val.instalacion_retiro == "1":
                        mat["tipo_trabajo_mat"] = "0"
                    elif val.instalacion_retiro == "0":
                        mat["tipo_trabajo_mat"] = "2"
                    elif val.instalacion_retiro == "2":
                        mat["tipo_trabajo_mat"] = "1"
                    elif val.instalacion_retiro == "3":
                        mat["tipo_trabajo_mat"]="6"

                    mat[ "codigo_mat" ] = val.codigo
                    mat[ "cantidad_replanteada" ] = val.cantidad
                    mat[ "aportacion" ] = Material.objects.filter( codigo_material = val.codigo ).first().aportacion

                    serializer_mat = NodoMATerializer( data = mat )
                    if serializer_mat.is_valid():
                        serializer_mat.save()

            EtlBudget.objects.filter( nodo__valorizacion = pk ).delete()

            mdo_val = NodoMDO.objects.filter(nodo__valorizacion=pk).all()
            sdata = [NodoMDOSerializer(mat_nodo).data for mat_nodo in mdo_val]

            # print(mdo_val) # Arreglo de objeto
            # print(sdata) # Arreglo de objetos serializados

            mat_val = NodoMAT.objects.filter(nodo__valorizacion=pk).all()
            sdata_m = [NodoMATerializer(mat_nodo).data for mat_nodo in mat_val]

            # Agrega el campo precio a cada item del arreglo
            for item in sdata:
                item['precio'] = Prestacion.objects.filter(codigo_prestacion = item["codigo_mdo"]).first().precio_prestacion

            for item in sdata_m:
                item['precio']=Material.objects.filter(codigo_material=item["codigo_mat"]).first().precio

            ordenar_mdo = sorted(sdata, key=lambda x: x['nodo'])
            grupos_mdo_por_nodos = groupby(ordenar_mdo, key=lambda x: x['nodo'])
            mano_obra_por_nodo=[{'nodo':nodo, 'valor_total':sum(t['cantidad_replanteada']*t['precio'] for t in trabajos)} for nodo, trabajos in grupos_mdo_por_nodos]

            ordenar_mat=sorted(sdata_m, key = lambda x: x['nodo'])
            m_grupos_mat_por_nodos=groupby(ordenar_mat, key=lambda x: x['nodo'])
            material_por_nodo=[{'nodo':nodo, 'valor_total':sum(t['cantidad_replanteada']*t['precio'] for t in trabajos)} for nodo, trabajos in m_grupos_mat_por_nodos]

            # Actualizar el valor de los nodos
            for nodo in mano_obra_por_nodo:
                nodo_actualizar = Nodo.objects.filter(id_nodo = nodo['nodo']).first()
                nodo_actualizar.valor_mano_obra = nodo['valor_total']
                nodo_actualizar.save()
            
            for nodo in material_por_nodo:
                nodo_actualizar = Nodo.objects.filter(id_nodo=nodo['nodo']).first()
                nodo_actualizar.valor_materiales = nodo['valor_total']
                nodo_actualizar.save()

            objeto = {}
            totales_mdo = list( map(lambda i : i["cantidad_replanteada"] * i["precio"], sdata ) )
            if totales_mdo != []:
                objeto["monto_mano_obra"] = functools.reduce(lambda tot, i:tot+i, totales_mdo)
            else:
                 objeto["monto_mano_obra"]=0

            totales_mat = list( map( lambda i : i[ "cantidad_replanteada" ] * i[ "precio" ], sdata_m ) )

            if totales_mat!=[]:
                objeto["monto_materiales"]=functools.reduce(lambda tot, i:tot+i, totales_mat)
                objeto["fecha_valorizacion"]=timezone.now()
            else:
                objeto["monto_materiales"]=0
                objeto["fecha_valorizacion"]=timezone.now()


            response=Valorizacion.objects.actualizar_valorizacion(objeto, pk)
            return Response({'message': f'El presupuesto {response} fue actualizados'}, 200)

        except Exception as e:
            mensaje = str(e)
            status_code = 412  #e.status_code
            return Response({'error': mensaje}, status=status_code)


class ListarNodosTrabajoView(ListAPIView):
    serializer_class = NodoSerializer
    def get_queryset(self):
            usuario = ValidateUser(self.request)
            if usuario:
                id_control=self.kwargs.get('pk')
                response = Nodo.objects.filter(valorizacion__id_valorizacion=id_control).all()
                return response
            
            return usuario


class ObtenerDetalleNodoView(RetrieveAPIView):
    serializer_class = NodoSerializer

    def get_queryset(self):
        usuario = ValidateUser(self.request)

        if usuario:
            id_valorizacion = self.kwargs.get('pk')
            queryset = Valorizacion.objects.obtener_detalle_trabajo(id_valorizacion)
            return queryset
        
        return usuario


class ListarNodosLclView(ListAPIView):
    serializer_class=NodoSerializer
    def get_queryset(self):
            token=self.request.COOKIES.get('jwt')
            if not token:
                raise AuthenticationFailed("Unauthenticated!")
            try:
                payload=jwt.decode(token,'secret',algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("Unauthenticated!")

            vlcls=self.request.query_params.get('vlcls','')
            vect_lcls=vlcls.split(',')

            # 1. ODM asociadas a cierta LCL
            v_odms=[]
            for lcl in vect_lcls:
                dato=Lcl.objects.filter(lcl=lcl).all()
                vodms=[odm for l in dato for odm in l.odms.all()]
                for odm in vodms:
                    if odm in v_odms:
                        pass
                    else:
                        v_odms.append(odm)
            
            
            # 2. Valorizaicones asociadas a cierta ODM
            v_val=list(set([od.valorizacion for od in v_odms]))
            print(v_val)

            # 3. Listar los nodos Asociados a las valorizaciones
            v_nodos=[]
            for val in v_val:
                nodos=Nodo.objects.filter(valorizacion=val).all()
                for nodo in nodos:
                    if nodo in v_nodos:
                        pass
                    else:
                        v_nodos.append(nodo)

            # print(v_nodos)
            
            # response=Nodo.objects.filter(valorizacion__id_valorizacion=lcl).all()
            return v_nodos


class ListarPrestaionesValorizacionView(ListAPIView):
    pass


class ListarMaterialesValorizacionView(ListAPIView):
    pass