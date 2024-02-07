from django.db import models

# Modelos auxiliares
from ..models.programacion import Programacion
from ..models.valorizacion import Nodo

class NodoSeguimiento(models.Model):

    ESTADO_CHOICES=(
        ('0','Parcial'),
        ('1','Completo'),
        ('2','Cancelado'),
    )

    nodo=models.ForeignKey( Nodo, on_delete=models.PROTECT)
    programacion = models.ForeignKey(Programacion, on_delete=models.PROTECT)
    programado=models.CharField(max_length=1,choices=ESTADO_CHOICES)
    ejecutado=models.CharField(max_length=1,choices=ESTADO_CHOICES, blank=True, null=True)
    facturado=models.BooleanField(blank=True, null=True)

    class Meta:
        unique_together=('nodo','programacion')