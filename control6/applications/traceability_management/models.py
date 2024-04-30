from django.db import models
from ..work_management.models import Trabajo
from ..inspecciones_tqi.models import ManiobrasTqi
from ..users_management.models import User
from .managers import TrazabilidadTrabajoManager, TrazabilidadInspeccionesTqiManager


class TrazabilidadTrabajo(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.PROTECT, related_name="trazabilidad_trabajo")
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="trazabilidad_usuario")
    fecha_trazabilidad = models.DateTimeField(auto_now=False, auto_now_add=False)
    comentario_trazabilidad = models.TextField()

    objects = TrazabilidadTrabajoManager()

    def __str__(self) -> str:
        return self.comentario_trazabilidad


class TrazabilidadInspeccionesTqi(models.Model):
    maniobra = models.ForeignKey(ManiobrasTqi, on_delete=models.PROTECT, related_name="trazabilidad_maniobra")
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="trazabilidad_usuario_maniobra")
    fecha_trazabilidad = models.DateTimeField(auto_now=False, auto_now_add=False)
    comentario_trazabilidad = models.TextField()

    objects = TrazabilidadInspeccionesTqiManager()

    def __str__(self) -> str:
        return self.comentario_trazabilidad