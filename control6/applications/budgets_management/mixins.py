from rest_framework.response import Response
from ..lcl_management.models import Lcl
from .models import Valorizacion
from ..odm_management.models import Odm
from ..scheduling_management.models import Programacion
import pandas as pd
import functools
from itertools import groupby
from .serializers import ( 
    # CrearValorizacion, 
    ValorizacionSerializer, 
    NodoSerializer, 
    EtlBudgetSerializer,
    NodoMDOSerializer, 
    NodoMATerializer, 
    # CrearNodoRG12Serializer, 
    CrearNodoRG10Serializer,
    NodoSerializer
)
from ..budgets_management.models import (
    Valorizacion, 
    Nodo,
    NodoMAT,
    NodoMDO,
    EtlBudget
)
import os
from django.conf import settings

class CargarFormatoReplanteoMixin(object):

    def validar_formato(self, libro):
        nombre_libro = libro.name
        if nombre_libro.endswith('.xls') or nombre_libro.endswith('.xlsx') or nombre_libro.endswith('.xlsm'):
            try:
                pd.read_excel(libro)
                return True
            except Exception as e:
                return False
        else:
            return False
        
    def validar_rg(self, libro):
        hojas = pd.read_excel(libro, sheet_name = None)
        if hojas.get("RG10_SER") is not None:
            return {"es_formato_rg":True, "formato":"RG10"} 
        elif hojas.get("RG11_node") is not None:
            return {"es_formato_rg":True, "formato":"RG11"}
        elif hojas.get("RG12_defectos") is not None:
            return {"es_formato_rg":True, "formato":"RG12"}
        else:
            return {"es_formato_rg":False}

    def cargar_rg10(self, libro, serializer):
        hoja_nodos = pd.read_excel(libro, sheet_name="NODOS", header=0)
        if hoja_nodos is not None:
            for index, row in hoja_nodos.iterrows():

                if str(row["Latitud\n(Inicial)"])!="nan":

                    nodo = {}
                    nodo["valorizacion"] = serializer.data["id_valorizacion"]
                    nodo["nodo"] = str(int(row["Nodo"]))
                    nodo["latitud_inicial"] = str(row["Latitud\n(Inicial)"])
                    nodo["longitud_inicial"] = str(row["Longitud\n(inicial)"])
                    nodo["punto_fisico_inicial"] = row["Punto Fisico Inicial"]

                    serializer_nodo = CrearNodoRG10Serializer(data=nodo)
                    if serializer_nodo.is_valid():
                        serializer_nodo.save()
                    
        hoja_presupuesto = pd.read_excel(libro, sheet_name="RG10_SER", header=2)
        if hoja_presupuesto is not None:
            for index, row in hoja_presupuesto.iterrows():
                mdo = {}
                nodo = CrearNodoRG10Serializer(Nodo.objects.filter(valorizacion=serializer.data["id_valorizacion"], nodo=str(int(row["NODO"]))).first())
                mdo["nodo"]=nodo.data["id_nodo"]

                if row["MOVIMIENTO "]=="Retiro":
                    mdo["tipo_trabajo_mdo"]="0"
                elif row["MOVIMIENTO "]=="Instalación":
                    mdo["tipo_trabajo_mdo"]="1"
                elif row["MOVIMIENTO "]=="Cambio":
                    mdo["tipo_trabajo_mdo"]="2"
                elif row["MOVIMIENTO "]=="Otro":
                    mdo["tipo_trabajo_mdo"]="3"

                mdo["codigo_mdo"] = str(row["PRESTACIÓN"])
                mdo["cantidad_replanteada"] = str(row["CANTIDAD"])
                serializer_mdo = NodoMDOSerializer(data=mdo)
                if serializer_mdo.is_valid():
                    serializer_mdo.save()

        hoja_presupuesto = pd.read_excel(libro, sheet_name="RG36_MAT", header=2)
        if hoja_presupuesto is not None:
            for index, row in hoja_presupuesto.iterrows():
                mat = {}
                nodo = CrearNodoRG10Serializer(Nodo.objects.filter(valorizacion=serializer.data["id_valorizacion"],nodo=str(int(row["NODO"]))).first())
                mat["nodo"]=nodo.data["id_nodo"]

                if row["MOVIMIENTO"] == "I N":
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

                mat["codigo_mat"] = str(row["CÓDIGO MATERIAL E4E"])
                mat["cantidad_replanteada"] = str(row["CANTIDAD"])

                serializer_mat = NodoMATerializer(data=mat)
                if serializer_mat.is_valid():
                    serializer_mat.save()

    def cargar_rg11(self, libro, serializer):
        hoja_nodos = pd.read_excel( libro, sheet_name = "RG11_node", header=5)      
        if hoja_nodos is not None:
            for index, row in hoja_nodos.iterrows():

                nodo = {}
                nodo[ "valorizacion" ]                = serializer.data["id_valorizacion"]
                nodo[ "nodo" ]                        = str( row[ "nodo" ] )
                nodo[ "latitud_inicial" ]             = str( row[ "latitud inicial" ] )
                nodo[ "longitud_inicial" ]            = str( row[ "longitud inicial" ] )
                nodo[ "latitud_final" ]               = row["latitud final"]
                nodo[ "longitud_final" ]              = row["longitud final"]
                nodo[ "punto_fisico_final" ]          = row["punto fisico inicial"]
                nodo[ "punto_fisico_inicial" ]        = row["punto fisico final"]
                nodo[ "norma_codensa_punto_inicial" ] = row["norma codensa punto inicial"]
                nodo[ "norma_codensa_punto_final" ]   = row["norma codensa punto final"]
                nodo[ "tramo" ]                       = ""
                nodo[ "cod_seccion" ]                 = ""
                nodo[ "cod_defecto" ]                 = ""
                nodo[ "valor_mano_obra" ]             = 0
                nodo[ "valor_materiales" ]            = 0
                nodo[ "id_mare" ]                     = ""

                if row[ "tipo instalacion" ] == "Aereo":
                    nodo["tipo_instalacion"] = "0"
                elif row[ "tipo instalacion" ] == "Subterraneo":
                    nodo["tipo_instalacion"] = "1"

                if row[ "tipo nodo" ] == "nodo_red":
                    nodo[ "tipo_nodo" ] = "0"
                elif row[ "tipo nodo" ] == "tramo_red":
                    nodo[ "tipo_nodo" ] = "1"
                elif row[ "tipo nodo" ] == "equipo":
                    nodo[ "tipo_nodo" ] = "2"
                elif row[ "tipo nodo" ] == "trafo":
                    nodo[ "tipo_nodo" ] = "3"
                elif row[ "tipo nodo" ] == "camara_sub":
                    nodo[ "tipo_nodo" ] = "4"
                elif row[ "tipo nodo" ] == "tramo_canalizacion":
                    nodo[ "tipo_nodo" ] = "5"
                elif row[ "tipo nodo" ] == "ramming":
                    nodo[ "tipo_nodo" ] = "6"
                elif row[ "tipo nodo" ] == "cercha":
                    nodo[ "tipo_nodo" ] = "7"

                if row[ 'nivel tension' ] == "34.5kV":
                    nodo[ "nivel_tension" ] = "N3_34.5"
                elif row[ 'nivel tension' ] == "13.2kV":
                    nodo[ "nivel_tension" ] = "N2_13.2"
                elif row[ 'nivel tension' ] == "11.4kV":
                    nodo[ "nivel_tension" ] = "N2_11.4"
                elif row[ 'nivel tension' ] == "208V":
                    nodo[ "nivel_tension" ] = "N1_208"

                serializer_nodo = NodoSerializer(data=nodo)
                if serializer_nodo.is_valid():
                    serializer_nodo.save()

        hoja_presupuesto = pd.read_excel( libro, sheet_name="RG11_budget", header=4)
        if hoja_presupuesto is not None:
            errores_budget = []
            for index, row in hoja_presupuesto.iterrows():
                if str(row["nodo"]) == "nan" or str ( row[ "nodo" ] ) == "":
                    break

                budget = {}
                nodo = Nodo.objects.filter(valorizacion = serializer.data["id_valorizacion"], nodo=str(row["nodo"])).first()

                if nodo is None:
                    errores_budget.append( { "Hoja 'RG11_budget': error en la fila '{}'".format( index + 6 ) : "El nodo '{}' no se encuentra en la hoja de nodos 'RG11_node'".format( str( row[ "nodo" ] ) ) })
                    continue

                budget[ "nodo" ] = nodo
                if row["tipo trabajo"]=="Retiro":
                    budget["instalacion_retiro"]="0"
                elif row["tipo trabajo"]=="Instalacion":
                    budget["instalacion_retiro"]="1"
                elif row["tipo trabajo"]=="Traslado":
                    budget["instalacion_retiro"]="2"
                elif row["tipo trabajo"]=="Otro":
                        budget["instalacion_retiro"]="3"

                budget["codigo"] = str( row[ "cod_prest/mat" ] )
                budget["cantidad"] = str( row[ "quantity" ] )
                budget["mat_mdo"] = "0"
                budget["aportacion"] = False

                serializer_budget = EtlBudgetSerializer( data  = budget )
                if serializer_budget.is_valid():
                    serializer_budget.save()
                else:
                    errores_budget.append({"Hoja 'RG11_budget': error en la fila '{}'".format(index + 6): "El item '{}' se encuentra duplicado en el nodo '{}'".format(str( row["cod_prest/mat"]), str(row["nodo"]))})

    def cargar_rg12(self, libro, serializer):
        hoja_nodos = pd.read_excel( libro, sheet_name ="RG12_defectos", header=4)

        if hoja_nodos is not None:
            operacion_nodo = {}

            for index, row in hoja_nodos.iterrows():
                nodo = {}
                nodo["valorizacion"] = serializer.data["id_valorizacion"]
                nodo["nodo"] = str(row["id_mare"])
                nodo["latitud_inicial"] = str(row["latitud"])
                nodo["longitud_inicial"] = str(row["longitud"])
                nodo["latitud_final"] = ""
                nodo["longitud_final"] = ""
                nodo["punto_fisico_final"] = row["punto fisico"]
                nodo["punto_fisico_inicial"] = ""
                nodo["norma_codensa_punto_inicial"] = row["norma"]
                nodo["norma_codensa_punto_final"]  = ""
                nodo["tipo_nodo"] = ""
                nodo["tipo_instalacion"] = ""
                nodo["tramo"] = str(row['tramo'])
                nodo["cod_seccion"] = str(row['cod_seccion'])
                nodo["cod_defecto"] = str(row[ 'cod_defecto'])
                nodo["valor_mano_obra"] = 0
                nodo["valor_materiales"] = 0
                nodo["id_mare"] = str(row['id_mare'])

                if row['nivel_tension' ] == "34.5kV":
                    nodo["nivel_tension"] = "N3_34.5"
                elif row['nivel_tension'] == "13.2kV":
                    nodo["nivel_tension"] = "N2_13.2"
                elif row['nivel_tension'] == "11.4kV":
                    nodo["nivel_tension"] = "N2_11.4"
                elif row['nivel_tension'] == "208V":
                    nodo["nivel_tension"] = "N1_208"

                operacion_nodo[str(int(row["item"]))] = str(row['tipo_trabajo'])

                serializer_nodo = NodoSerializer(data=nodo)
                if serializer_nodo.is_valid():
                    serializer_nodo.save()

        hoja_presupuesto = pd.read_excel(libro, sheet_name="RG12_budget", header=4)

        if hoja_presupuesto is not None:
            errores_budget = {}
    
            for index, row in hoja_presupuesto.iterrows():

                if str (row["id_mare"]) == "nan" or str (row["id_mare"]) == "":
                    break

                budget = {}
                nodo = Nodo.objects.filter(valorizacion = serializer.data["id_valorizacion"], nodo = str(row["id_mare"])).first()

                if nodo is None:
                    errores_budget.append({ "Hoja 'RG12_budget': error en la fila '{}'".format(index + 6) : "El defecto '{}' no se encuentra en la hoja de nodos 'RG12_node'".format(str( row[ "id_mare" ]))})
                    continue

                budget["nodo"] = nodo
                if operacion_nodo[str(int(row["item"]))] == "Retiro":
                    budget["instalacion_retiro"]="0"
                elif operacion_nodo[str(int(row["item"]))] == "Instalacion":
                    budget["instalacion_retiro"]="1"
                elif operacion_nodo[str(int(row["item"]))] == "Instalacion":
                    budget["instalacion_retiro"]="2"
                elif operacion_nodo[str(int(row["item"]))] == "Otro":
                        budget["instalacion_retiro"]="3"

                budget["codigo"] = str(row["cod_prest/mat"] )
                budget["cantidad"] = str(row["quantity"])
                budget["mat_mdo"] = "0"
                budget["aportacion"] = False

                serializer_budget = EtlBudgetSerializer(data=budget)
                if serializer_budget.is_valid():
                    serializer_budget.save()
                else:
                    if errores_budget == {}:
                        errores_budget['message'] = "Hoja 'RG11_budget': Error en la fila '{}'".format(index + 6) + "," +  "El item '{}' se encuentra duplicado en el nodo '{}'".format(str(row["cod_prest/mat"]), str(row[ "id_mare"]))
                    else:
                        errores_budget['message'] = errores_budget['message'] + ", Hoja 'RG11_budget': Error en la fila '{}'".format(index + 6) + "," +  "El item '{}' se encuentra duplicado en el nodo '{}'".format(str(row["cod_prest/mat"]), str(row[ "id_mare"]))

            if errores_budget != {}:
                errores_budget['eliminar'] = True
                return errores_budget
            else:
                return ({"eliminar":False,"id_valorizacion":serializer.data["id_valorizacion"]})

class EliminarValorizacionMixin(object):
    def eliminiarValorizacion(self, valorizacion):
        valorizacion_eliminar = Valorizacion.objects.filter(id_valorizacion=valorizacion).first()

        print(valorizacion_eliminar)

        ruta_archivo=os.path.join(settings.MEDIA_ROOT, str(valorizacion_eliminar.presupuesto))
        if os.path.exists(ruta_archivo):
            os.remove(ruta_archivo)
        valorizacion_eliminar.delete()

    def eliminarNodos(self, valorizacion):
        nodos_relacionados = Nodo.objects.filter(valorizacion=valorizacion).all()
        for nodo in nodos_relacionados:
            mdos_relacionadas=NodoMDO.objects.filter(nodo=nodo).all()
            for mdo in mdos_relacionadas:
                mdo.delete()
            mats_relacionados=NodoMAT.objects.filter(nodo=nodo).all()
            for mat in mats_relacionados:
                mat.delete()

            etl_relacionados=EtlBudget.objects.filter(nodo=nodo).all()
            for etl in etl_relacionados:
                etl.delete()
            nodo.delete()