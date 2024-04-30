from django.db import models

from django.db import models
from ..models.nivel_tension import NivelTension
from ..models.subestacion import Subestacion
from ..managers.circuito_manager import CircuitoManager


    from django.db import models
from ..models.nivel_tension import NivelTension
from ..managers.subestacion_manager import SubestacionManager
from ...static_data.models.unidad_territorial import UnidadTerritorial


class NivelTension(models.Model):
    nivel = models.CharField(max_length=8, primary_key=True)
    rango = models.CharField(max_length=80)
    valor_nominal_v = models.FloatField()
    
    objects=NivelTensionManager()


class Subestacion(models.Model):
    codigo = models.CharField(primary_key=True, max_length=2)
    nombre = models.CharField(max_length=150)
    nivel_tension = models.ForeignKey(NivelTension, on_delete=models.PROTECT, related_name="nt")
    unidades_territoriales = models.ManyToManyField(UnidadTerritorial)

    objects=SubestacionManager()



class Circuito(models.Model):
    codigo_circuito = models.CharField(primary_key=True,max_length=8)
    ubicacion_tecnica = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    subestacion = models.ForeignKey(Subestacion, on_delete=models.CASCADE)
    tesniones_nominales = models.ManyToManyField(NivelTension)
    longitud_aerea_mt = models.PositiveIntegerField()
    logitud_subterranea_mt = models.PositiveIntegerField()
    cantidad_clientes = models.PositiveIntegerField()
    cantidad_trafos = models.PositiveIntegerField(blank=True, null= True)
    
    objects = CircuitoManager()


