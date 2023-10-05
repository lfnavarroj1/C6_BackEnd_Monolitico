from django.db import models

from ..managers.nivel_tension_manager import NivelTensionManager

# Create your models here.

class NivelTension(models.Model):
    nivel=models.CharField(max_length=8, primary_key=True)
    rango=models.CharField(max_length=80)
    valor_nominal_v=models.FloatField()

    objects=NivelTensionManager()
