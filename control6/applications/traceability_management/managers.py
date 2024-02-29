from django.db import models
from rest_framework.response import Response
from django.utils import timezone
from ..work_management.models import Trabajo

class TrazabilidadTrabajoManager(models.Manager):
    def registrar_trazabilidad(self, req, usuario):
        datos = {}
        # datos["trabajo"] = Trabajo.objects.get(pk=req["trabajo"])
        datos["trabajo"] = req["trabajo"]
        datos["usuario"] = usuario
        datos["fecha_trazabilidad"] = timezone.now()
        datos["comentario_trazabilidad"] = req["comentario_trazabilidad"]
        trazabilidad = self.create(**datos)
        return Response({'message': f'La trazabilidad {trazabilidad} fue agregada'}, status=201)
    
    def obtener_trazabilidad(self, id_control):
        trab = Trabajo.objects.get(pk=id_control)
        result = self.filter(trabajo=trab)
        return result
    
class TrazabilidadInspeccionesTqiManager(models.Manager):
    def registrar_trazabilidad(self,req,usuario):
        datos = {}
        datos["maniobra"] = Trabajo.objects.get(pk=req["trabajo"])
        datos["usuario"] = usuario
        datos["fecha_trazabilidad"] = timezone.now()
        datos["comentario_trazabilidad"] = req["comentario_trazabilidad"]
        trazabilidad = self.create(**datos)
        return Response({'message': f'La trazabilidad {trazabilidad} fue agregada'}, status=201)
    
    def obtener_trazabilidad(self, id_control):
        trab = Trabajo.objects.get(pk=id_control)
        result = self.filter(trabajo=trab)
        return result