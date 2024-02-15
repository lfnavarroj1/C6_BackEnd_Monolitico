from django.db import models
from .unidad_territorial import UnidadTerritorial


class Contrato(models.Model):
    numero_contrato = models.CharField(primary_key=True, max_length=12)
    nombre = models.CharField(max_length=250,  blank=True, null=True)
    objeto = models.CharField(max_length=750,  blank=True, null=True)
    unidades_territoriales = models.ManyToManyField(UnidadTerritorial, related_name='contratos_operacion_territorial',  blank=True, null=True)
    gestoria = models.ForeignKey(UnidadTerritorial, on_delete=models.PROTECT, related_name='contrato_gestoria', blank=True, null=True)
    activo = models.BooleanField(blank=True, null=True)

