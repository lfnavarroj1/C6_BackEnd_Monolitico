from django.db import models
from .proceso import Proceso
from .estado_trabajo import EstadoTrabajo

# Create your models here.
class ModuloBandeja(models.Model):
    id_modulo=models.CharField(primary_key=True,max_length=4)
    nombre=models.CharField(max_length=20)

class RutaProceso(models.Model):
    codigo_ruta=models.CharField(primary_key=True,max_length=8)
    proceso=models.ForeignKey(Proceso, on_delete=models.PROTECT)
    modulos=models.ManyToManyField(ModuloBandeja)
    paso = models.CharField(max_length=2)
    estado = models.ForeignKey(EstadoTrabajo, on_delete=models.PROTECT)
    
