from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from ..static_data.models.proceso import Proceso
from ..static_data.models.estado_trabajo import EstadoTrabajo
from ..static_data.models.contrato import Contrato


# from .managers import UserManager

class C6Modules(models.Model):
    id_module=models.CharField(unique=True, primary_key=True)
    name=models.CharField(max_length=120)
    description=models.CharField(max_length=255)

# Create your models here.

class User(AbstractUser):
    username=models.CharField(max_length=11, unique=True, primary_key=True)
    assigned=models.CharField(max_length=50, unique=True)
    password=models.CharField(max_length=255)
    phone_number=models.CharField(max_length=15)
    procesos=models.ManyToManyField(Proceso, blank=True, related_name="user_process")
    estado_trabajo=models.ManyToManyField(EstadoTrabajo,blank=True)
    user_modules=models.ManyToManyField(C6Modules,blank=True)
    contrato= models.ForeignKey(Contrato, on_delete=models.PROTECT, blank=True,null=True)

    USERNAME_FIELD='username'
    REQUIRED_FIELDS=[]

    # objects = UserManager()

    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.first_name + " " +self.last_name

