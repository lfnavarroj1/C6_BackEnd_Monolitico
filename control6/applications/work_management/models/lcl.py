from django.db import models
from .odm import Odm

# Create your models here.

class Lcl(models.Model):
    ESTADOS_LCL=(
        ('0','LIBERACION OPERATIVA'),
        ('1','ENVIAR A SCM'),
        ('2','EN SCM'),
        ('3','FACTURADA'),
    )
    INDICADOR_IMP=(
        ('WC','INVERSION'),
        ('WK','WK - GASTO'),
        ('WI','WI - GASTO'),
    )

    numero_lcl = models.BigIntegerField(primary_key=True)
    estado_lcl = models.CharField(max_length=1,choices=ESTADOS_LCL)
    indicador_impuesto = models.CharField(max_length=2, choices=INDICADOR_IMP)
    valor_mano_obra=models.FloatField()
    valor_materiales=models.FloatField()
    responsable_scm=models.CharField(max_length=50)
    texto_scm=models.CharField(max_length=250)
    alcance = models.TextField()
    odms=models.ManyToManyField(Odm)
    