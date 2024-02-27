from django.db import models

class Material(models.Model):
    codigo_material = models.CharField(max_length=10,primary_key=True)
    descripcion = models.CharField(max_length=50)
    unidad_medida = models.CharField(max_length=5)
    aportacion = models.BooleanField()
    precio = models.FloatField()