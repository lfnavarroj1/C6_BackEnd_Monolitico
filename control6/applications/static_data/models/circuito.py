from django.db import models
from ..models.nivel_tension import NivelTension
from ..models.subestacion import Subestacion
from ..managers.circuito_manager import CircuitoManager

# Create your models here.

class Circuito(models.Model):
    codigo_circuito=models.CharField(primary_key=True,max_length=8)
    ubicacion_tecnica = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    subestacion = models.ForeignKey(Subestacion, on_delete=models.CASCADE)
    tesniones_nominales=models.ManyToManyField(NivelTension)
    longitud_aerea_mt=models.PositiveIntegerField()
    logitud_subterranea_mt = models.PositiveIntegerField()
    cantidad_clientes = models.PositiveIntegerField()
    
    objects=CircuitoManager()
