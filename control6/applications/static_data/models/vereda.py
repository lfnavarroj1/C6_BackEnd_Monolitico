from django.db import models
from .municipio import Municipio

class Vereda(models.Model):
    codigo_vereda=models.CharField(max_length=10, primary_key=True)
    nombre_vereda=models.CharField(max_length=60)
    municipio=models.ForeignKey(Municipio, on_delete=models.PROTECT)
    factor_dispersion=models.CharField(max_length=2)