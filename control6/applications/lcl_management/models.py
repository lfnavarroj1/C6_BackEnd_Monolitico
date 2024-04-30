from django.db import models
from ..odm_management.models import Odm
from ..users_management.models import User
from .manager import LclManager

class Lcl(models.Model):
    ESTADOS_LCL = (
        ('0','LIBERACION OPERATIVA'),
        ('1','ENVIAR A SCM'),
        ('2','EN SCM'),
        ('3','FACTURADA'),
        ('4','ANULADA'),
    )
    
    INDICADOR_IMP = (
        ('WC','INVERSION'),
        ('WK','WK - GASTO'),
        ('WI','WI - GASTO'),
    )

    lcl = models.BigIntegerField(primary_key=True)
    estado_lcl = models.CharField(max_length=1,choices=ESTADOS_LCL)
    indicador_impuesto = models.CharField(max_length=2, choices=INDICADOR_IMP)
    valor_mano_obra = models.FloatField()
    valor_materiales = models.FloatField()
    responsable_scm = models.ForeignKey(User,on_delete=models.PROTECT)
    texto_scm = models.TextField()
    alcance = models.TextField()
    odms = models.ManyToManyField(Odm)

    objects = LclManager()
    