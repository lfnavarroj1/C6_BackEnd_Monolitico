from django.db import models


class TerritorialUnit(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=60)


class Municipality(models.Model):
    code = models.CharField(max_length=6, primary_key=True)  
    name = models.CharField(max_length=50)
    territorial_unit = models.ManyToManyField(TerritorialUnit)


class Sidewalk(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=60)
    municipality = models.ForeignKey(Municipality, on_delete=models.PROTECT)
    cft = models.CharField(max_length=7)
    dispersion_factor = models.CharField(max_length=2)

    