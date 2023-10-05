from django.db import models
from ...users.models import User

class UnidadTerritorial(models.Model):
    numero=models.CharField(max_length=2, primary_key=True)
    nombre=models.CharField(max_length=60)
    jefe=models.ForeignKey(User, on_delete=models.PROTECT)
   