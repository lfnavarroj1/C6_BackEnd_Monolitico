from django.db import models
from .unidad_territorial import UnidadTerritorial

class Municipio(models.Model):
    codigo_municipio=models.CharField(max_length=6, primary_key=True)
    nombre=models.CharField(max_length=50)
    unidad_territorial=models.ForeignKey(UnidadTerritorial,on_delete=models.PROTECT)