from django.db import models
from .trabajo import Trabajo
from ...users.models import User
from ..managers.trazabilidad_manager import TrazabilidadManager

# Import managers

class Trazabilidad(models.Model):
    trabajo = models.ForeignKey(Trabajo, on_delete=models.PROTECT, related_name="trazabilidad_trabajo")
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="trazabilidad_usuario")
    fecha_trazabilidad = models.DateTimeField(auto_now=False, auto_now_add=False)
    comentario_trazabilidad = models.TextField()

    objects=TrazabilidadManager()

    def __str__(self) -> str:
        return self.comentario_trazabilidad