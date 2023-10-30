from django.db import models
from ...work_management.models.valorizacion import Valorizacion
from ..managers.odm_manager import OdmManager

# Create your models here.

class Odm(models.Model):
    odm = models.BigIntegerField(primary_key=True)
    valorizacion = models.ForeignKey(Valorizacion, on_delete=models.PROTECT)
    agp = models.BigIntegerField()
    protocolo=models.BigIntegerField()
    solicitud = models.BigIntegerField()

    objects=OdmManager()
