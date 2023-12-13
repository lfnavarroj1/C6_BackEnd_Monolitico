from django.db import models
from ..static_data.models.contrato import Contrato

# Create your models here.

class Prestacion(models.Model):
    GRUPOMERCOLOGICO=(
        ("0","SLTR2600"),
        ("1","LELE0501"),
        ("2","LELE0600"),
        ("3","LELE0502"),
        ("4","LEII0900"),
        ("5","FEGE0200"),
        ("6","MELE0200"),
        ("7","LELE0504"),
        ("8","SRTS2200"),
    )
    codigo_prestacion=models.CharField(max_length=8, primary_key=True)
    codigo_elenco=models.CharField(max_length=8)
    texto_prestacion=models.TextField()
    alcance=models.TextField()
    unidad_medida=models.CharField(max_length=5, blank=True, null=True)
    posicion=models.CharField(max_length=3)
    factor_dispersion=models.CharField(max_length=4)
    grupo_mercologico=models.CharField(max_length=1,choices=GRUPOMERCOLOGICO)
    precion_prestacion=models.FloatField() # Corregir 
    contrato=models.ForeignKey(Contrato,on_delete=models.PROTECT)




