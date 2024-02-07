from django.db import models
from ..managers.process_manager import ProcesoManager

# Create your models here.

class Proceso(models.Model):
    codigo_proceso=models.CharField(primary_key=True,max_length=8)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=350)
    ejecucion_ticket=models.BooleanField(null=True, blank=True)

    objects=ProcesoManager()

