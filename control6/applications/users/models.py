from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    id=models.CharField(max_length=15, unique=True, primary_key=True)
    password=models.CharField(max_length=255)
    assigned=models.CharField(max_length=50, unique=True)
    phone_number=models.CharField(max_length=15)
    username=None

    USERNAME_FIELD='id'


