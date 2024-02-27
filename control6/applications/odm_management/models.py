from django.db import models
from budgets_management.models import Valorizacion
from .manager import OdmManager

# Create your models here.

class Odm(models.Model):
    odm = models.BigIntegerField(primary_key=True)
    valorizacion = models.ForeignKey(Valorizacion, on_delete=models.PROTECT)
    agp = models.BigIntegerField()
    protocolo=models.BigIntegerField()
    solicitud = models.BigIntegerField()

    objects=OdmManager()
