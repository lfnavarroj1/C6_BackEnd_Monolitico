from django.db import models

# Create your models here.

class Contrato(models.Model):
    numero_contrato=models.CharField(primary_key=True,max_length=12)
    nombre = models.CharField(max_length=50)
    objeto = models.CharField(max_length=250)

