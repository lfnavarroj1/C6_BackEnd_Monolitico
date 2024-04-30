from django.db import models
from ..location_management.models import TerritorialUnit


class Contrat(models.Model):
    code = models.CharField(primary_key=True, max_length=12)
    name = models.CharField(max_length=250,  blank=True, null=True)
    objetive = models.CharField(max_length=750,  blank=True, null=True)
    territorial_units = models.ManyToManyField(TerritorialUnit)
    management_unit = models.ForeignKey(TerritorialUnit, on_delete=models.PROTECT, related_name='contrat_menegemer', blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)


class TechnicalTeam(models.Model):

    PROCESS_GROUP_TYPE = (
        ('0','PROGRAMADO'),
        ('1','NO PROGRAMADO'),
        ('2','TELECONTROL'),
    )

    code = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=25)
    process_group = models.CharField(max_length=1, choices=PROCESS_GROUP_TYPE, null=True, blank=True)
    contrat = models.ForeignKey(Contrat, on_delete=models.PROTECT, null=True, blank=True)
