from django.db import models

class EstructuraPresupuestal(models.Model):
    id_estructura_pptal = models.CharField(max_length=25, primary_key=True)
    nombre_corto = models.CharField(max_length=20)
    anio = models.CharField(max_length=4)	
    macrocategoria = models.CharField(max_length=15)
    ir = models.CharField(max_length=2)
    proyecto = models.CharField(max_length=50)
    indicador_impuesto = models.CharField(max_length=2)
