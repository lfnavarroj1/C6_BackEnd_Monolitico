from django.db import models
# Create your models here.
from ...static_data.models.contrato import Contrato

class Cuadrilla(models.Model):

    GRUPO_PROCESO=(
        ('0','PROGRAMADO'),
        ('1','NO PROGRAMADO'),
        ('2','TELECONTROL'),
    )

    codigo_cuadrilla=models.CharField(primary_key=True,max_length=8)
    nombre = models.CharField(max_length=50)
    tipo_cuadrilla = models.CharField(max_length=25)
    grupo_proceso=models.CharField(max_length=1, choices=GRUPO_PROCESO, null=True, blank=True)
    contrato=models.ForeignKey(Contrato, on_delete=models.PROTECT, null=True, blank=True)




