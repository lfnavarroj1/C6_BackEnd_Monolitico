from django.db import models
# from django.db.models import Q
# from ...users.models import User
from rest_framework.response import Response
from django.utils import timezone
from ..models.trabajo import Trabajo

class TrazabilidadManager(models.Manager):
    def registrar_trazabilidad(self,req,usuario):
        datos={}
        datos["trabajo"]=Trabajo.objects.get(pk=req["trabajo"])
        datos["usuario"]=usuario
        datos["fecha_trazabilidad"]=timezone.now()
        datos["comentario_trazabilidad"]=req["comentario_trazabilidad"]
        trazabilidad=self.create(**datos) #Falta implementar manejo de excepciones
        return Response({'message': f'La trazabilidad {trazabilidad} fue agregada'}, status=201)
    
    def obtener_trazabilidad(self,id_control):
        trab=Trabajo.objects.get(pk=id_control)
        result=self.filter(trabajo=trab)
        return result