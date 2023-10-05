from django.db import models

# Create your models here.

class Odm(models.Model):
    odm = models.BigIntegerField(primary_key=True)
    valorizacion = models.CharField(max_length=23)
    agp = models.BigIntegerField()
    protocolo=models.BigIntegerField()
    solicitud = models.BigIntegerField()
    tiene_lcl=models.BooleanField()
