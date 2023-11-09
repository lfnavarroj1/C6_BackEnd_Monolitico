from django.db import models
# from django.db.models import Q
# from ...users.models import User
from rest_framework.response import Response
# from django.utils import timezone
from ..models.valorizacion import Valorizacion

class OdmManager(models.Manager):
    def registrar_odm(self,req):

        datos={}
        datos["odm"]=req["odm"]
        datos["valorizacion"]=Valorizacion.objects.get(pk=req["valorizacion"])
        datos["agp"]=req["agp"]
        datos["protocolo"]=req["protocolo"]
        datos["solicitud"]=req["solicitud"]
        odm=self.create(**datos) # Falta implementar manejo de excepciones
        return Response({'message': f'La ODM {odm} fue agregada'}, status=201)
    
    def obtener_odms(self,id_control):
        result=self.filter(valorizacion__trabajo__id_control=id_control)
        return result
    

    def actualizar_odm(self, odm_data,odm):
        odm_actual=self.get(pk=odm)

        campos_actualizables=[
            "agp",
            "protocolo",
            "solicitud",
        ]

        # CAMPOS RELACIONADOS
        for campo in campos_actualizables:
            if campo in odm_data:
                setattr(odm_actual,campo,odm_data[campo])

        odm_actual.save()
        return odm_actual