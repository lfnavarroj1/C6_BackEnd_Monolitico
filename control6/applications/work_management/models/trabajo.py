from django.db import models
from django.utils import timezone
from ..managers.trabajo_manager import TrabajoManager

# Create your models here.
class Trabajo(models.Model):


    id_control = models.CharField(primary_key=True, max_length=20, unique=True, default="N/A", editable=False)
    pms_quotation = models.CharField(max_length=50)
    pms_need = models.CharField(max_length=50)
    proceso = models.CharField(max_length=8)
    caso_radicado = models.CharField(max_length=50)
    estado_trabajo = models.CharField(max_length=8)
    alcance = models.TextField()
    estructura_presupuestal = models.CharField(max_length=25)
    priorizacion = models.DateField(auto_now=False, auto_now_add=False)
    unidad_territorial=models.CharField(max_length=2)
    municipio = models.CharField(max_length=6)
    vereda = models.CharField(max_length=10)
    direccion = models.CharField(max_length=120)
    subestacion = models.CharField(max_length=2)
    circuito = models.CharField(max_length=8)
    contrato = models.CharField(max_length=12)

    objects=TrabajoManager()

    def save(self, *args, **kwargs):
        if self.id_control == "N/A":
            current_year = timezone.now().year
            last_instance = Trabajo.objects.filter(id_control__startswith=f'C6-{current_year}-').order_by('-id_control').first()

            if last_instance:
                last_id = int(last_instance.id_control.split('-')[-1])
                next_id = last_id + 1
            else:
                next_id = 1

            self.id_control = f'C6-{current_year}-{str(next_id).zfill(6)}'

        super(Trabajo, self).save(*args, **kwargs)
    

    def __str__(self):
        return self.id_control
