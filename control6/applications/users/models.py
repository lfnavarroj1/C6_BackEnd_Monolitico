from django.db import models
from django.contrib.auth.models import AbstractUser

from ..static_data.models.proceso import Proceso
from ..static_data.models.estado_trabajo import EstadoTrabajo
from ..static_data.models.contrato import Contrato
from ..static_data.models.unidad_territorial import UnidadTerritorial


class C6Modules(models.Model):
    id_module = models.CharField(unique=True, primary_key=True)
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=255)
    url_modulo = models.CharField(max_length=200, blank=True,null=True)


class User(AbstractUser):
    username = models.CharField(max_length=11, unique=True, primary_key=True)
    assigned = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    procesos = models.ManyToManyField(Proceso, blank=True, related_name="user_process")
    estado_trabajo = models.ManyToManyField(EstadoTrabajo, blank=True)
    user_modules = models.ManyToManyField(C6Modules, blank=True)
    unidades_territoriales = models.ManyToManyField(UnidadTerritorial, blank=True)
    contratos = models.ManyToManyField(Contrato, blank=True)
    cargo = models.CharField(max_length=150, blank=True, null=True)
    lider_hse = models.BooleanField(blank=True, null=True)
    es_enel = models.BooleanField(blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.first_name + " " + self.last_name


