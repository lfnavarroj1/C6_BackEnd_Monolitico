from django.db import models
from .lcl import Lcl
from ...static_data.models.cuadrilla import Cuadrilla
from django.utils import timezone

class Programacion(models.Model):
    ESTADO_PROGRA=(
        ('0','Sin maniobra'),
        ('1','Con maniobra no aprobada'),
        ('2','Con maniobra aprobada'),
    )
    id_programcion = models.CharField(primary_key=True, max_length=25, unique=True, default="N/A", editable=False)
    fecha_ejecucion = models.DateField(auto_now=False, auto_now_add=False)
    cuadrilla= models.ForeignKey(Cuadrilla, on_delete=models.PROTECT)
    lcl = models.ForeignKey(Lcl, on_delete=models.PROTECT)
    alcance = models.TextField()
    estado=models.CharField(max_length=1,choices=ESTADO_PROGRA)

    def save(self, *args, **kwargs):
        if self.id_programcion == "N/A":
            current_year = timezone.now().year
            last_instance = Programacion.objects.filter(id_programcion__startswith=f'PR-{current_year}-').order_by('-id_programcion').first()

            if last_instance:
                last_id = int(last_instance.id_programcion.split('-')[-1])
                next_id = last_id + 1
            else:
                next_id = 1

            self.id_programcion = f'PR-{current_year}-{str(next_id).zfill(2)}'

        super(Programacion, self).save(*args, **kwargs)

    def __str__(self):
        return self.id_programcion