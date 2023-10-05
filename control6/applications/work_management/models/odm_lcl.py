from django.db import models

class OdmLcl(models.Model):
    valoracion=models.CharField(max_length=20)
    odm=models.CharField(max_length=20)

    class Meta:
        unique_together=(("valoracion","odm"),)