from django.db import models
from ..models.nivel_tension import NivelTension
from ..managers.subestacion_manager import SubestacionManager
from ...static_data.models.unidad_territorial import UnidadTerritorial

class Subestacion(models.Model):
    codigo = models.CharField(primary_key=True, max_length=2)
    nombre = models.CharField(max_length=150)
    nivel_tension = models.ForeignKey(NivelTension, on_delete=models.PROTECT, related_name="nt")
    unidades_territoriales = models.ManyToManyField(UnidadTerritorial)

    objects=SubestacionManager()
