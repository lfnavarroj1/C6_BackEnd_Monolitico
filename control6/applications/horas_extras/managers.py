from django.db import models
# from django.db.models import Q
from rest_framework.response import Response
from ..users.models import User


class HorasExtrasManager(models.Manager):
    def registrar_hora_extra(self,req,usuario):
        datos={}
        datos["usuario"]=usuario
        datos["fecha"]=req["fecha"]
        datos["hora_entrada"]=req["hora_entrada"]
        datos["hora_salida"]=req["hora_salida"]
        datos["observacion"]=req["observacion"]
        datos["estado"]=req["estado"]

        hora_extra=self.create(**datos)

        # print(req["lcls"])

        # lista_lcls=list(map(int,req["lcls"].split(',')))
        # lista_cuadrillas=list(map(str,req["cuadrillas"].split(',')))

        # programacion.lcls.set(Lcl.objects.filter(pk__in=lista_lcls))
        # programacion.cuadrillas.set(Cuadrilla.objects.filter(pk__in=lista_cuadrillas))

        # datos["cuadrilla"]=Cuadrilla.objects.get(pk=req["cuadrilla"])
        # datos["lcl"]=Lcl.objects.get(pk=req["lcl"])

        return Response({'message': f'La {hora_extra} fue agregada con éxito'}, status=201)
    
    def obtener_horas_extras(self,user):
        result=self.filter(usuario=user).all()
        return result
    

    def actualizar_horas_extras(self, he_data,id_he):
        he_actual=self.get(pk=id_he)

        campos_actualizables=[
            "usuario",
            "fecha",
            "hora_entrada",
            "hora_salida",
            "observacion",
            "estado",
        ]

        # CAMPOS RELACIONADOS
        for campo in campos_actualizables:
            if campo in he_data:
                setattr(he_actual,campo,he_data[campo])
        
        he_actual.save()
        return he_actual