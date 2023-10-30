from django.db import models
from .odm import Odm
from ...users.models import User
from ..managers.lcl_manager import LclManager

# Create your models here.

class Lcl(models.Model):
    ESTADOS_LCL=( # Estados LCL - Crear Clase
        ('0','LIBERACION OPERATIVA'),
        ('1','ENVIAR A SCM'),
        ('2','EN SCM'),
        ('3','FACTURADA'),
        ('4','ANULADA'),
    )
    INDICADOR_IMP=( # Estado Indicador de IMP - Crear Clase
        ('WC','INVERSION'),
        ('WK','WK - GASTO'),
        ('WI','WI - GASTO'),
    )

    lcl = models.BigIntegerField(primary_key=True)
    estado_lcl = models.CharField(max_length=1,choices=ESTADOS_LCL)
    indicador_impuesto = models.CharField(max_length=2, choices=INDICADOR_IMP)
    valor_mano_obra=models.FloatField()
    valor_materiales=models.FloatField()
    responsable_scm=models.ForeignKey(User,on_delete=models.PROTECT)
    texto_scm=models.TextField()
    alcance = models.TextField()
    odms=models.ManyToManyField(Odm)

    objects=LclManager()
    