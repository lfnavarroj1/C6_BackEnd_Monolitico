from rest_framework import status
from rest_framework.generics import (
    ListAPIView, 
    CreateAPIView, 
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView
    )
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.valorizacion import Valorizacion, Nodo
from ..serializers.valorizacion_serializer import CrearValorizacion, ValorizacionSerializer, CrearNodoSerializer, CrearNodoMDOSerializer, CrearNodoMATerializer, CrearNodoRG12Serializer, CrearNodoRG10Serializer
from ..models.trabajo import Trabajo
from rest_framework.exceptions import AuthenticationFailed
import jwt,json, os #, datetime
from ...users.models import User

from django.http import FileResponse, HttpResponse
from django.conf import settings
from ..models.valorizacion import NodoMAT,NodoMDO
from ...prestaciones.models import Prestacion
from ...materiales.models import Material

# import magic
import mimetypes
import pandas as pd
import functools

from django.utils import timezone


# 1. SUBIR FORMATO DE PRESUPUESTO DE UN TRABAJOS ----------------------------------------------------------------------------
class CargarValorizacionView(APIView):
    def post(self, request, *args, **kwargs):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        # usuario=User.objects.get(username=payload['username'])
        # presupuesto = request.data.get('presupuesto') 

        # Crear una instancia del modelo SoportesIniciales con el archivo
        data=request.data
        id_trabajo=data['trabajo']
        data['trabajo']=Trabajo.objects.get(pk=id_trabajo)

        serializer = CrearValorizacion(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # 1. Validar el formato que se está cargando.
            hojas_excel=pd.read_excel(data['presupuesto'], sheet_name=None)
            if hojas_excel.get("RG11_node") is not None:
                formato="RG11"
            elif hojas_excel.get("RG12_defectos") is not None:
                formato="RG12"
            elif hojas_excel.get("RG10_SER") is not None:
                formato="RG10"


            if formato=="RG11":
                hoja_nodos=pd.read_excel(data['presupuesto'], sheet_name="RG11_node", header=5)      
                if hoja_nodos is not None:
                    for index, row in hoja_nodos.iterrows():

                        nodo={}
                        nodo["valorizacion"]=serializer.data["id_valorizacion"]
                        nodo["nodo"]=str(int(row["nodo"]))
                        nodo["latitud_inicial"]=str(row["latitud inicial"])
                        nodo["longitud_inicial"]=str(row["longitud inicial"])
                        nodo["latitud_final"]=row["latitud final"]
                        nodo["longitud_final"]=row["longitud final"]
                        nodo["punto_fisico_inicial"]=row["punto fisico inicial"]
                        nodo["punto_fisico_final"]=row["punto fisico final"]
                        nodo["norma_codensa_punto_inicial"]=row["norma codensa punto inicial"]
                        nodo["norma_codensa_punto_final"]=row["norma codensa punto final"]

                        # Definiendo el nodo
                        if row["tipo instalacion"]=="Aereo":
                            nodo["tipo_instalacion"]="0"
                        elif row["tipo instalacion"]=="Aereo":
                            nodo["tipo_instalacion"]="1"

                        # Definiendo el tipo de instalción
                        if row["tipo nodo"]=="nodo_red":
                            nodo["tipo_nodo"]= "0"
                        elif row["tipo nodo"]=="tramo_red":
                            nodo["tipo_nodo"]= "1"
                        elif row["tipo nodo"]=="equipo":
                            nodo["tipo_nodo"]= "2"
                        elif row["tipo nodo"]=="trafo":
                            nodo["tipo_nodo"]= "3"
                        elif row["tipo nodo"]=="camara_sub":
                            nodo["tipo_nodo"]= "4"
                        elif row["tipo nodo"]=="tramo_canalizacion":
                            nodo["tipo_nodo"]= "5"
                        elif row["tipo nodo"]=="ramming":
                            nodo["tipo_nodo"]= "6"
                        elif row["tipo nodo"]=="cercha":
                            nodo["tipo_nodo"]= "7"

                        nodo["nivel_tesion"]=data['nivel_tension']

                        serializer_nodo = CrearNodoSerializer(data=nodo)
                        if serializer_nodo.is_valid():
                            serializer_nodo.save()

                # Extraer datos del formato.
                hoja_presupuesto=pd.read_excel(data['presupuesto'], sheet_name="RG11_budget", header=4)
                if hoja_presupuesto is not None:
                    
                    for index, row in hoja_presupuesto.iterrows():

                        if str(row["MO-MAT"])=="MO":
                            mdo={}
                            nodo=CrearNodoSerializer(Nodo.objects.filter(valorizacion=serializer.data["id_valorizacion"], nodo=str(int(row["nodo"]))).first()) 
                            mdo["nodo"]=nodo.data["id_nodo"]

                            if row["tipo trabajo"]=="Retiro":
                                mdo["tipo_trabajo_mdo"]="0"
                            elif row["tipo trabajo"]=="Instalacion":
                                mdo["tipo_trabajo_mdo"]="1"
                            elif row["tipo trabajo"]=="Traslado":
                                mdo["tipo_trabajo_mdo"]="2"
                            elif row["tipo trabajo"]=="Otro":
                                mdo["tipo_trabajo_mdo"]="3"

                            mdo["codigo_mdo"]=str(row["cod_prest/mat"])
                            mdo["cantidad"]=str(row["quantity"])

                            serializer_mdo = CrearNodoMDOSerializer(data=mdo)
                            if serializer_mdo.is_valid():
                                serializer_mdo.save()

                        elif str(row["MO-MAT"])=="MAT":
                                mat={}
                                nodo=CrearNodoSerializer(Nodo.objects.filter(valorizacion=serializer.data["id_valorizacion"], nodo=str(int(row["nodo"]))).first()) 
                                mat["nodo"]=nodo.data["id_nodo"]

                                if row["tipo trabajo"]=="Instalacion":
                                    mat["tipo_trabajo_mat"]="0"
                                elif row["tipo trabajo"]=="Retiro":
                                    mat["tipo_trabajo_mat"]="2"
                                elif row["tipo trabajo"]=="Traslado":
                                    mat["tipo_trabajo_mat"]="1"
                                elif row["tipo trabajo"]=="Otro":
                                    mat["tipo_trabajo_mat"]="6"

                                mat["codigo_mat"]=str(row["cod_prest/mat"])
                                mat["cantidad"]=str(row["quantity"])

                                serializer_mat = CrearNodoMATerializer(data=mat)
                                if serializer_mat.is_valid():
                                    serializer_mat.save()

            elif formato=="RG12":
                hoja_nodos=pd.read_excel(data['presupuesto'], sheet_name="RG12_defectos", header=4)
                if hoja_nodos is not None:

                    operacion_nodo={}

                    for index, row in hoja_nodos.iterrows():

                        nodo={}
                        nodo["valorizacion"]=serializer.data["id_valorizacion"]
                        nodo["nodo"]=str(int(row["item"]))
                        nodo["latitud_inicial"]=str(row["latitud"])
                        nodo["longitud_inicial"]=str(row["longitud"])
                        nodo["punto_fisico_inicial"]=row["punto fisico"]
                        nodo["norma_codensa_punto_inicial"]=row["norma"]

                        if row['nivel_tension']=="34.5kV":
                            nodo["nivel_tesion"]="N3_34.5"
                        elif row['nivel_tension']=="13.2kV":
                            nodo["nivel_tesion"]="N2_13.2"
                        elif row['nivel_tension']=="11.4kV":
                            nodo["nivel_tesion"]="N2_11.4"
                        elif row['nivel_tension']=="208V":
                            nodo["nivel_tesion"]="N1_208"

                        nodo["tramo"]=str(row['tramo'])
                        nodo["cod_seccion"]=str(row['cod_seccion'])
                        nodo["cod_defecto"]=str(row['cod_defecto'])
                        nodo["id_mare"]=str(row['id_mare'])

                        operacion_nodo[str(int(row["item"]))]=str(row['tipo_trabajo'])

                        serializer_nodo = CrearNodoRG12Serializer(data=nodo)
                        if serializer_nodo.is_valid():
                            serializer_nodo.save()

                # 1.1. Sacar datos de la hoja RG12_budget
                hoja_presupuesto=pd.read_excel(data['presupuesto'], sheet_name="RG12_budget", header=4)
                if hoja_presupuesto is not None:
                
                    for index, row in hoja_presupuesto.iterrows():

                        if str(row["TIPO"])=="MO":
                            mdo={}
                            nodo=CrearNodoRG12Serializer(Nodo.objects.filter(valorizacion=serializer.data["id_valorizacion"],nodo=str(int(row["item"]))).first())
                            mdo["nodo"]=nodo.data["id_nodo"]

                            # mdo["tipo_trabajo_mdo"]="1"
                            if operacion_nodo[str(int(row["item"]))]=="Retiro":
                                mdo["tipo_trabajo_mdo"]="0"
                            elif operacion_nodo[str(int(row["item"]))]=="Instalacion":
                                mdo["tipo_trabajo_mdo"]="1"
                            elif operacion_nodo[str(int(row["item"]))]=="Traslado":
                                mdo["tipo_trabajo_mdo"]="2"
                            elif operacion_nodo[str(int(row["item"]))]=="Otro":
                                mdo["tipo_trabajo_mdo"]="3"


                            mdo["codigo_mdo"]=str(row["cod_prest/mat"])
                            mdo["cantidad"]=str(row["quantity"])

                            serializer_mdo = CrearNodoMDOSerializer(data=mdo)
                            if serializer_mdo.is_valid():
                                serializer_mdo.save()

                        elif str(row["TIPO"])=="MAT":
                                mat={}
                                nodo=CrearNodoRG12Serializer(Nodo.objects.filter(valorizacion=serializer.data["id_valorizacion"],nodo=str(int(row["item"]))).first())
                                mat["nodo"]=nodo.data["id_nodo"]

                                if operacion_nodo[str(int(row["item"]))]=="Retiro":
                                    mat["tipo_trabajo_mat"]="2"
                                elif operacion_nodo[str(int(row["item"]))]=="Instalacion":
                                    mat["tipo_trabajo_mat"]="0"
                                elif operacion_nodo[str(int(row["item"]))]=="Traslado":
                                    mat["tipo_trabajo_mat"]="1"
                                elif operacion_nodo[str(int(row["item"]))]=="Otro":
                                    mat["tipo_trabajo_mat"]="6"

                                mat["codigo_mat"]=str(row["cod_prest/mat"])
                                mat["cantidad"]=str(row["quantity"])

                                serializer_mat = CrearNodoMATerializer(data=mat)
                                if serializer_mat.is_valid():
                                    serializer_mat.save()

            elif formato=="RG10":

                hoja_nodos=pd.read_excel(data['presupuesto'], sheet_name="NODOS", header=0)

                if hoja_nodos is not None:

                    for index, row in hoja_nodos.iterrows():
                        if str(row["Latitud\n(Inicial)"])!="nan":

                            nodo={}
                            nodo["valorizacion"]=serializer.data["id_valorizacion"]
                            nodo["nodo"]=str(int(row["Nodo"]))
                            nodo["latitud_inicial"]=str(row["Latitud\n(Inicial)"])
                            nodo["longitud_inicial"]=str(row["Longitud\n(inicial)"])
                            nodo["punto_fisico_inicial"]=row["Punto Fisico Inicial"]

                            serializer_nodo = CrearNodoRG10Serializer(data=nodo)
                            if serializer_nodo.is_valid():
                                serializer_nodo.save()

                hoja_presupuesto=pd.read_excel(data['presupuesto'], sheet_name="RG10_SER", header=2)
                if hoja_presupuesto is not None:
                    print(hoja_presupuesto.columns)
                    for index, row in hoja_presupuesto.iterrows():
                       
                        mdo={}
                        nodo=CrearNodoRG10Serializer(Nodo.objects.filter(valorizacion=serializer.data["id_valorizacion"],nodo=str(int(row["NODO"]))).first())
                        mdo["nodo"]=nodo.data["id_nodo"]

                        if row["MOVIMIENTO "]=="Retiro":
                            mdo["tipo_trabajo_mdo"]="0"
                        elif row["MOVIMIENTO "]=="Instalación":
                            mdo["tipo_trabajo_mdo"]="1"
                        elif row["MOVIMIENTO "]=="Cambio":
                            mdo["tipo_trabajo_mdo"]="2"
                        elif row["MOVIMIENTO "]=="Otro":
                            mdo["tipo_trabajo_mdo"]="3"

                        mdo["codigo_mdo"]=str(row["PRESTACIÓN"])
                        mdo["cantidad"]=str(row["CANTIDAD"])
                        serializer_mdo = CrearNodoMDOSerializer(data=mdo)
                        if serializer_mdo.is_valid():
                            serializer_mdo.save()

                hoja_presupuesto=pd.read_excel(data['presupuesto'], sheet_name="RG36_MAT", header=2)
                if hoja_presupuesto is not None:

                    for index, row in hoja_presupuesto.iterrows():
                        mat={}
                        nodo=CrearNodoRG10Serializer(Nodo.objects.filter(valorizacion=serializer.data["id_valorizacion"],nodo=str(int(row["NODO"]))).first())
                        mat["nodo"]=nodo.data["id_nodo"]

                        if row["MOVIMIENTO"]=="I N":
                            mat["tipo_trabajo_mat"]="0"
                        elif row["MOVIMIENTO"]=="I RZ":
                            mat["tipo_trabajo_mat"]="1"
                        elif row["MOVIMIENTO"]=="R CH":
                            mat["tipo_trabajo_mat"]="2"
                        elif row["MOVIMIENTO"]=="R RZ":
                            mat["tipo_trabajo_mat"]="3"
                        elif row["MOVIMIENTO"]=="M A":
                            mat["tipo_trabajo_mat"]="4"
                        elif row["MOVIMIENTO"]=="HURTO":
                            mat["tipo_trabajo_mat"]="5"
                        elif row["MOVIMIENTO"]=="N O":
                            mat["tipo_trabajo_mat"]="6"

                        mat["codigo_mat"]=str(row["CÓDIGO MATERIAL E4E"])
                        mat["cantidad"]=str(row["CANTIDAD"])

                        serializer_mat = CrearNodoMATerializer(data=mat)
                        if serializer_mat.is_valid():
                            serializer_mat.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ----------------------------------------------------------------------------------------------------------------------


# 2. LISTAR PRESUPUESTOS CARGADOS A UN TRABAJO -------------------------------------------------------------------------
class ListarValorizacion(ListAPIView):
    serializer_class=ValorizacionSerializer
    def get_queryset(self):
        token=self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        id_control=self.kwargs.get('pk')
        response=Valorizacion.objects.filter(trabajo__id_control=id_control).all()
        return response
# ----------------------------------------------------------------------------------------------------------------------


# 3. OBTENER EL DETALLE DE UN PRESUPUESTO ----------------------------------------
class ObtenerValorizacion(RetrieveAPIView):
    serializer_class = ValorizacionSerializer

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
        queryset = Valorizacion.objects.filter(id_valorizacion=pk)
        return queryset
# -------------------------------------------------------------------------------


# 4. ACTUALIZAR UN PRESUPUESTO ------------------------------------------------------
class ActualizarValorizacion(UpdateAPIView):
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

        if "presupuesto" in request.data:
            nodos_relacionados=Nodo.objects.filter(valorizacion=pk).all()
            print(nodos_relacionados)
            for nodo in nodos_relacionados:
                mdos_relacionadas=NodoMDO.objects.filter(nodo=nodo).all()
                for mdo in mdos_relacionadas:
                    mdo.delete()
                mats_relacionados=NodoMAT.objects.filter(nodo=nodo).all()
                for mat in mats_relacionados:
                    mat.delete()
                nodo.delete()
        

        try:
            response=Valorizacion.objects.actualizar_valorizacion(request.data, pk)

            if "presupuesto" in request.data:
                # 1. Validar el formato que se está cargando.
                hojas_excel=pd.read_excel(request.data['presupuesto'], sheet_name=None)
                if hojas_excel.get("RG11_node") is not None:
                    formato="RG11"
                elif hojas_excel.get("RG12_defectos") is not None:
                    formato="RG12"
                elif hojas_excel.get("RG10_SER") is not None:
                    formato="RG10"

                if formato=="RG11":
                    hoja_nodos=pd.read_excel(request.data['presupuesto'], sheet_name="RG11_node", header=5)      
                    if hoja_nodos is not None:
                        for index, row in hoja_nodos.iterrows():

                            nodo={}
                            nodo["valorizacion"]=pk
                            nodo["nodo"]=str(int(row["nodo"]))
                            nodo["latitud_inicial"]=str(row["latitud inicial"])
                            nodo["longitud_inicial"]=str(row["longitud inicial"])
                            nodo["latitud_final"]=row["latitud final"]
                            nodo["longitud_final"]=row["longitud final"]
                            nodo["punto_fisico_inicial"]=row["punto fisico inicial"]
                            nodo["punto_fisico_final"]=row["punto fisico final"]
                            nodo["norma_codensa_punto_inicial"]=row["norma codensa punto inicial"]
                            nodo["norma_codensa_punto_final"]=row["norma codensa punto final"]

                            # Definiendo el nodo
                            if row["tipo instalacion"]=="Aereo":
                                nodo["tipo_instalacion"]="0"
                            elif row["tipo instalacion"]=="Aereo":
                                nodo["tipo_instalacion"]="1"

                            # Definiendo el tipo de instalción
                            if row["tipo nodo"]=="nodo_red":
                                nodo["tipo_nodo"]= "0"
                            elif row["tipo nodo"]=="tramo_red":
                                nodo["tipo_nodo"]= "1"
                            elif row["tipo nodo"]=="equipo":
                                nodo["tipo_nodo"]= "2"
                            elif row["tipo nodo"]=="trafo":
                                nodo["tipo_nodo"]= "3"
                            elif row["tipo nodo"]=="camara_sub":
                                nodo["tipo_nodo"]= "4"
                            elif row["tipo nodo"]=="tramo_canalizacion":
                                nodo["tipo_nodo"]= "5"
                            elif row["tipo nodo"]=="ramming":
                                nodo["tipo_nodo"]= "6"
                            elif row["tipo nodo"]=="cercha":
                                nodo["tipo_nodo"]= "7"

                            nodo["nivel_tesion"]=request.data['nivel_tension']

                            serializer_nodo = CrearNodoSerializer(data=nodo)
                            if serializer_nodo.is_valid():
                                serializer_nodo.save()

                    # Extraer datos del formato.
                    hoja_presupuesto=pd.read_excel(request.data['presupuesto'], sheet_name="RG11_budget", header=4)
                    if hoja_presupuesto is not None:
                        
                        for index, row in hoja_presupuesto.iterrows():

                            if str(row["MO-MAT"])=="MO":
                                mdo={}
                                nodo=CrearNodoSerializer(Nodo.objects.filter(valorizacion=pk, nodo=str(int(row["nodo"]))).first()) 
                                mdo["nodo"]=nodo.data["id_nodo"]

                                if row["tipo trabajo"]=="Retiro":
                                    mdo["tipo_trabajo_mdo"]="0"
                                elif row["tipo trabajo"]=="Instalacion":
                                    mdo["tipo_trabajo_mdo"]="1"
                                elif row["tipo trabajo"]=="Traslado":
                                    mdo["tipo_trabajo_mdo"]="2"
                                elif row["tipo trabajo"]=="Otro":
                                    mdo["tipo_trabajo_mdo"]="3"

                                mdo["codigo_mdo"]=str(row["cod_prest/mat"])
                                mdo["cantidad"]=str(row["quantity"])

                                serializer_mdo = CrearNodoMDOSerializer(data=mdo)
                                if serializer_mdo.is_valid():
                                    serializer_mdo.save()

                            elif str(row["MO-MAT"])=="MAT":
                                    mat={}
                                    nodo=CrearNodoSerializer(Nodo.objects.filter(valorizacion=pk, nodo=str(int(row["nodo"]))).first()) 
                                    mat["nodo"]=nodo.data["id_nodo"]

                                    if row["tipo trabajo"]=="Instalacion":
                                        mat["tipo_trabajo_mat"]="0"
                                    elif row["tipo trabajo"]=="Retiro":
                                        mat["tipo_trabajo_mat"]="2"
                                    elif row["tipo trabajo"]=="Traslado":
                                        mat["tipo_trabajo_mat"]="1"
                                    elif row["tipo trabajo"]=="Otro":
                                        mat["tipo_trabajo_mat"]="6"

                                    mat["codigo_mat"]=str(row["cod_prest/mat"])
                                    mat["cantidad"]=str(row["quantity"])

                                    serializer_mat = CrearNodoMATerializer(data=mat)
                                    if serializer_mat.is_valid():
                                        serializer_mat.save()

                elif formato=="RG12":
                    hoja_nodos=pd.read_excel(request.data['presupuesto'], sheet_name="RG12_defectos", header=4)
                    if hoja_nodos is not None:

                        operacion_nodo={}

                        for index, row in hoja_nodos.iterrows():

                            nodo={}
                            nodo["valorizacion"]=pk
                            nodo["nodo"]=str(int(row["item"]))
                            nodo["latitud_inicial"]=str(row["latitud"])
                            nodo["longitud_inicial"]=str(row["longitud"])
                            nodo["punto_fisico_inicial"]=row["punto fisico"]
                            nodo["norma_codensa_punto_inicial"]=row["norma"]

                            if row['nivel_tension']=="34.5kV":
                                nodo["nivel_tesion"]="N3_34.5"
                            elif row['nivel_tension']=="13.2kV":
                                nodo["nivel_tesion"]="N2_13.2"
                            elif row['nivel_tension']=="11.4kV":
                                nodo["nivel_tesion"]="N2_11.4"
                            elif row['nivel_tension']=="208V":
                                nodo["nivel_tesion"]="N1_208"

                            nodo["tramo"]=str(row['tramo'])
                            nodo["cod_seccion"]=str(row['cod_seccion'])
                            nodo["cod_defecto"]=str(row['cod_defecto'])
                            nodo["id_mare"]=str(row['id_mare'])

                            operacion_nodo[str(int(row["item"]))]=str(row['tipo_trabajo'])

                            serializer_nodo = CrearNodoRG12Serializer(data=nodo)
                            if serializer_nodo.is_valid():
                                serializer_nodo.save()

                    # 1.1. Sacar datos de la hoja RG12_budget
                    hoja_presupuesto=pd.read_excel(request.data['presupuesto'], sheet_name="RG12_budget", header=4)
                    if hoja_presupuesto is not None:
                    
                        for index, row in hoja_presupuesto.iterrows():

                            if str(row["TIPO"])=="MO":
                                mdo={}
                                nodo=CrearNodoRG12Serializer(Nodo.objects.filter(valorizacion=pk,nodo=str(int(row["item"]))).first())
                                mdo["nodo"]=nodo.data["id_nodo"]

                                # mdo["tipo_trabajo_mdo"]="1"
                                if operacion_nodo[str(int(row["item"]))]=="Retiro":
                                    mdo["tipo_trabajo_mdo"]="0"
                                elif operacion_nodo[str(int(row["item"]))]=="Instalacion":
                                    mdo["tipo_trabajo_mdo"]="1"
                                elif operacion_nodo[str(int(row["item"]))]=="Traslado":
                                    mdo["tipo_trabajo_mdo"]="2"
                                elif operacion_nodo[str(int(row["item"]))]=="Otro":
                                    mdo["tipo_trabajo_mdo"]="3"


                                mdo["codigo_mdo"]=str(row["cod_prest/mat"])
                                mdo["cantidad"]=str(row["quantity"])

                                serializer_mdo = CrearNodoMDOSerializer(data=mdo)
                                if serializer_mdo.is_valid():
                                    serializer_mdo.save()

                            elif str(row["TIPO"])=="MAT":
                                    mat={}
                                    nodo=CrearNodoRG12Serializer(Nodo.objects.filter(valorizacion=pk,nodo=str(int(row["item"]))).first())
                                    mat["nodo"]=nodo.data["id_nodo"]

                                    if operacion_nodo[str(int(row["item"]))]=="Retiro":
                                        mat["tipo_trabajo_mat"]="2"
                                    elif operacion_nodo[str(int(row["item"]))]=="Instalacion":
                                        mat["tipo_trabajo_mat"]="0"
                                    elif operacion_nodo[str(int(row["item"]))]=="Traslado":
                                        mat["tipo_trabajo_mat"]="1"
                                    elif operacion_nodo[str(int(row["item"]))]=="Otro":
                                        mat["tipo_trabajo_mat"]="6"

                                    mat["codigo_mat"]=str(row["cod_prest/mat"])
                                    mat["cantidad"]=str(row["quantity"])

                                    serializer_mat = CrearNodoMATerializer(data=mat)
                                    if serializer_mat.is_valid():
                                        serializer_mat.save()

                elif formato=="RG10":

                    hoja_nodos=pd.read_excel(request.data['presupuesto'], sheet_name="NODOS", header=0)

                    if hoja_nodos is not None:

                        for index, row in hoja_nodos.iterrows():
                            if str(row["Latitud\n(Inicial)"])!="nan":

                                nodo={}
                                nodo["valorizacion"]=pk
                                nodo["nodo"]=str(int(row["Nodo"]))
                                nodo["latitud_inicial"]=str(row["Latitud\n(Inicial)"])
                                nodo["longitud_inicial"]=str(row["Longitud\n(inicial)"])
                                nodo["punto_fisico_inicial"]=row["Punto Fisico Inicial"]

                                serializer_nodo = CrearNodoRG10Serializer(data=nodo)
                                if serializer_nodo.is_valid():
                                    serializer_nodo.save()

                    hoja_presupuesto=pd.read_excel(request.data['presupuesto'], sheet_name="RG10_SER", header=2)
                    if hoja_presupuesto is not None:
                        print(hoja_presupuesto.columns)
                        for index, row in hoja_presupuesto.iterrows():
                        
                            mdo={}
                            nodo=CrearNodoRG10Serializer(Nodo.objects.filter(valorizacion=pk,nodo=str(int(row["NODO"]))).first())
                            mdo["nodo"]=nodo.data["id_nodo"]

                            if row["MOVIMIENTO "]=="Retiro":
                                mdo["tipo_trabajo_mdo"]="0"
                            elif row["MOVIMIENTO "]=="Instalación":
                                mdo["tipo_trabajo_mdo"]="1"
                            elif row["MOVIMIENTO "]=="Cambio":
                                mdo["tipo_trabajo_mdo"]="2"
                            elif row["MOVIMIENTO "]=="Otro":
                                mdo["tipo_trabajo_mdo"]="3"

                            mdo["codigo_mdo"]=str(row["PRESTACIÓN"])
                            mdo["cantidad"]=str(row["CANTIDAD"])
                            serializer_mdo = CrearNodoMDOSerializer(data=mdo)
                            if serializer_mdo.is_valid():
                                serializer_mdo.save()

                    hoja_presupuesto=pd.read_excel(request.data['presupuesto'], sheet_name="RG36_MAT", header=2)
                    if hoja_presupuesto is not None:

                        for index, row in hoja_presupuesto.iterrows():
                            mat={}
                            nodo=CrearNodoRG10Serializer(Nodo.objects.filter(valorizacion=pk,nodo=str(int(row["NODO"]))).first())
                            mat["nodo"]=nodo.data["id_nodo"]

                            if row["MOVIMIENTO"]=="I N":
                                mat["tipo_trabajo_mat"]="0"
                            elif row["MOVIMIENTO"]=="I RZ":
                                mat["tipo_trabajo_mat"]="1"
                            elif row["MOVIMIENTO"]=="R CH":
                                mat["tipo_trabajo_mat"]="2"
                            elif row["MOVIMIENTO"]=="R RZ":
                                mat["tipo_trabajo_mat"]="3"
                            elif row["MOVIMIENTO"]=="M A":
                                mat["tipo_trabajo_mat"]="4"
                            elif row["MOVIMIENTO"]=="HURTO":
                                mat["tipo_trabajo_mat"]="5"
                            elif row["MOVIMIENTO"]=="N O":
                                mat["tipo_trabajo_mat"]="6"

                            mat["codigo_mat"]=str(row["CÓDIGO MATERIAL E4E"])
                            mat["cantidad"]=str(row["CANTIDAD"])

                            serializer_mat = CrearNodoMATerializer(data=mat)
                            if serializer_mat.is_valid():
                                serializer_mat.save()


            return Response({'message': f'El presupuesto {response} fue actualizados'}, 200)
        except Exception as e:
            mensaje = str(e)
            status_code = 412  #e.status_code
            return Response({'error': mensaje}, status=status_code)

# -------------------------------------------------------------------------------

# 5.ELIMINAR UN PRESUPUESTO
class EliminarValorizacion(DestroyAPIView):
    def put(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
    queryset=Valorizacion.objects.all()
    serializer_class=ValorizacionSerializer
    lookup_field='pk'



    def eliminar_datos_relacionados(self,valorizacion):
        nodos_relacionados=Nodo.objects.filter(valorizacion=valorizacion).all()

        for nodo in nodos_relacionados:
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



# 5. CALCULAR VALOR DE MDO Y MAT DE ACUERDO A LO CARGADO --------------------------------
class CalcularValorizacion(UpdateAPIView):
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
            mdo_val=NodoMDO.objects.filter(nodo__valorizacion=pk).all()
            sdata=[CrearNodoMDOSerializer(mat_nodo).data for mat_nodo in mdo_val]

            mat_val=NodoMAT.objects.filter(nodo__valorizacion=pk).all()
            sdata_m=[CrearNodoMATerializer(mat_nodo).data for mat_nodo in mat_val]

            # Cargar el valor a cada diccionario
            for item in sdata:
                item['precio']=Prestacion.objects.filter(codigo_prestacion=item["codigo_mdo"]).first().precion_prestacion

            for item in sdata_m:
                item['precio']=Material.objects.filter(codigo_material=item["codigo_mat"]).first().precio


            objeto={}
            totales_mdo=list(map(lambda i:i["cantidad"]*i["precio"],sdata))
            if totales_mdo!=[]:
                objeto["monto_mano_obra"]=functools.reduce(lambda tot,i:tot+i, totales_mdo)
            else:
                 objeto["monto_mano_obra"]=0

            totales_mat=list(map(lambda i:i["cantidad"]*i["precio"],sdata_m))

            if totales_mat!=[]:
                objeto["monto_materiales"]=functools.reduce(lambda tot,i:tot+i, totales_mat)
                objeto["fecha_valorizacion"]=timezone.now()
            else:
                objeto["monto_materiales"]=0
                objeto["fecha_valorizacion"]=timezone.now()


            response=Valorizacion.objects.actualizar_valorizacion(objeto, pk)
            return Response({'message': f'El presupuesto {response} fue actualizados'}, 200)

            # return Response({'message': f'El presupuesto {mdo_val} fue actualizados'}, 200)
        except Exception as e:
            mensaje = str(e)
            status_code = 412  #e.status_code
            return Response({'error': mensaje}, status=status_code)

# -------------------------------------------------------------------------------