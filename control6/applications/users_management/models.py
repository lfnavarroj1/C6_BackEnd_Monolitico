from django.db import models
from django.contrib.auth.models import AbstractUser
from ..process_management.models import Process
from ..process_management.models import StateWork 
from ..location_management.models import TerritorialUnit
from ..contracts_management.models import Contrat

# from .managers import UsuarioManager


class C6Module(models.Model):
    id_module = models.CharField(unique=True, primary_key=True, max_length=200)
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=255)
    url_module = models.CharField(max_length=200, blank=True,null=True)


class User(AbstractUser):
    username = models.CharField(max_length=11, unique=True, primary_key=True)
    assigned = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    processes = models.ManyToManyField(Process, blank=True, related_name="user_process")
    managed_states = models.ManyToManyField(StateWork, blank=True)
    user_modules = models.ManyToManyField(C6Module, blank=True)
    territorial_units = models.ManyToManyField(TerritorialUnit, blank=True)
    contrats = models.ManyToManyField(Contrat, blank=True)
    cargo = models.CharField(max_length=150, blank=True, null=True)
    lider_hse = models.BooleanField(blank=True, null=True)
    es_enel = models.BooleanField(blank=True, null=True)

    # objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.first_name + " " + self.last_name


