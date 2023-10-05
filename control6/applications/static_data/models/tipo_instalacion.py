from django.db import models

class TipoInstalacion(models.Model):
    id_tipo=models.CharField(max_length=2, primary_key=True)
    nombre=models.CharField(max_length=60)
   