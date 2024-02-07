from django.db import models

from ..static_data.models.proceso import Proceso
from ..static_data.models.unidad_territorial import UnidadTerritorial 

class QProcesos(models.Model):
    unidad_territorial = models.ForeignKey(UnidadTerritorial, on_delete=models.PROTECT)
    proceso = models.ForeignKey(Proceso, on_delete=models.PROTECT)
    anio = models.PositiveIntegerField()
    mes = models.PositiveIntegerField()
    q_meta = models.PositiveIntegerField()
    q_proceso = models.PositiveIntegerField()
    q_ejecutada = models.PositiveIntegerField()
    q_facturado = models.PositiveIntegerField()


class PProcesos(models.Model):
    unidad_territorial = models.ForeignKey(UnidadTerritorial, on_delete=models.PROTECT)
    proceso = models.ForeignKey(Proceso, on_delete=models.PROTECT)
    anio = models.PositiveIntegerField()
    mes = models.PositiveIntegerField()
    p_meta = models.PositiveIntegerField()
    p_proceso = models.PositiveIntegerField()
    p_ejecutada = models.PositiveIntegerField()
    p_facturado = models.PositiveIntegerField()
