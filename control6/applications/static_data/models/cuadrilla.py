from django.db import models
# Create your models here.

class Cuadrilla(models.Model):
    codigo_cuadrilla=models.CharField(primary_key=True,max_length=8)
    nombre = models.CharField(max_length=50)
    tipo_cuadrilla = models.CharField(max_length=25)

