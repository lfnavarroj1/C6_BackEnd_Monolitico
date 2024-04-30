from django.db import models
from .managers import ProcessManager


class FrontendModule(models.Model):
    id = models.CharField(primary_key=True,max_length=4)
    name = models.CharField(max_length=20)


class Process(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=350)

    objects = ProcessManager()


class StateWork(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=350)


class WorkFlow(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    process = models.ForeignKey(Process, on_delete=models.PROTECT)
    modules = models.ManyToManyField(FrontendModule)
    step = models.CharField(max_length = 2)
    state_work = models.ForeignKey(StateWork, on_delete=models.PROTECT)
    

