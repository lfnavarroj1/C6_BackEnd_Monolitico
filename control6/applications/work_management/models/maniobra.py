from django.db import models
from .programacion import Programacion
from ..managers.maniobra_manager import ManiobraManager

class Maniobra(models.Model):
    TIPO_MANIOBRAS=(
        ('0','PDL'),
        ('1','PI'),
        ('2','PSTL'),
    )
    ESTADO_MANIOBRA=(
        ('0','PENDIENTE POR APROBAR'),
        ('1', 'APROBADO'),
        ('2', 'PARA CORREGIR'),
        ('3', 'EJECUTADO'),
    )
    maniobra=models.CharField(max_length=15, primary_key=True)
    programaciones = models.ManyToManyField(Programacion)
    tipo_maniobra=models.CharField(max_length=1,choices=TIPO_MANIOBRAS)
    alcance=models.TextField()
    fecha_inicio = models.DateField(auto_now=False, auto_now_add=False)
    fecha_fin = models.DateField(auto_now=False, auto_now_add=False)
    estado_maniobra=models.CharField(max_length=1,choices=ESTADO_MANIOBRA)

    objects=ManiobraManager()
