from django.db import models
# from django.db.models import Q
from ...users.models import User
from ...static_data.models.cuadrilla import Cuadrilla
from ..models.lcl import Lcl
from rest_framework.response import Response


class ProgramacionManager(models.Manager):
    def registrar_programacion(self,req):
        datos={}
        datos["fecha_ejecucion"]=req["fecha_ejecucion"]
        datos["alcance"]=req["alcance"]
        datos["estado"]=req["estado"]


        programacion=self.create(**datos)

        print(req["lcls"])

        lista_lcls=list(map(int,req["lcls"].split(',')))
        lista_cuadrillas=list(map(str,req["cuadrillas"].split(',')))

        programacion.lcls.set(Lcl.objects.filter(pk__in=lista_lcls))
        programacion.cuadrillas.set(Cuadrilla.objects.filter(pk__in=lista_cuadrillas))

        # datos["cuadrilla"]=Cuadrilla.objects.get(pk=req["cuadrilla"])
        # datos["lcl"]=Lcl.objects.get(pk=req["lcl"])

        return Response({'message': f'La {programacion} fue agregada con éxito'}, status=201)
    
    def obtener_programacion(self,id_control):
        result=self.filter(lcls__odms__valorizacion__trabajo__id_control=id_control).distinct()
        return result
    

    def actualizar_programacion(self, programacion_data,programacion):
        programacion_actual=self.get(pk=programacion)

        campos_actualizables=[
            "fecha_ejecucion",
            "cuadrillas",
            "lcls",
            "alcance",
            "estado",
        ]

        # CAMPOS RELACIONADOS
        for campo in campos_actualizables:
            if campo in programacion_data:
                if campo=="cuadrillas":
                    # setattr(programacion_actual,campo,Cuadrilla.objects.get(pk=programacion_data["cuadrilla"]))
                    lista_cuadrillas=list(map(str,programacion_data["cuadrillas"]))
                    programacion_actual.cuadrillas.set(Cuadrilla.objects.filter(pk__in=lista_cuadrillas))
                elif campo=="lcls":
                    lista_lcls=list(map(int,programacion_data["lcls"]))
                    programacion_actual.lcls.set(Lcl.objects.filter(pk__in=lista_lcls))
                    # setattr(programacion_actual,campo,Lcl.objects.get(pk=programacion_data["lcl"]))
                else:
                    setattr(programacion_actual,campo,programacion_data[campo])
        
        programacion_actual.save()
        return programacion_actual