from django.db import models

class EstadoTrabajo(models.Model):
    id_estado = models.CharField(primary_key=True, max_length=8)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=350)

