from django.db import models
from django.utils import timezone
from ...work_management.models.trabajo import Trabajo
from ...static_data.models.nivel_tension import NivelTension
from ..managers.valorizacion_manager import ValorizacionManager
# Create your models here.
import os

class Valorizacion(models.Model):

    ESTADO_CHOICES=(
        ('0','Revisión'),
        ('1','Rechazado'),
        ('2','Aprobado'),
        ('3','Aprobado con modificación'),
        ('4','Anulado'),
    )

    id_valorizacion=models.CharField(primary_key=True, max_length=23, unique=True, default="N/A", editable=False)
    trabajo = models.ForeignKey(Trabajo, on_delete=models.PROTECT)
    monto_mano_obra=models.FloatField()
    monto_materiales=models.FloatField()
    estado = models.CharField(max_length=1,choices=ESTADO_CHOICES)
    nivel_tension=models.ForeignKey(NivelTension, on_delete=models.PROTECT)
    presupuesto=models.FileField(upload_to='presupuesto',blank=True, null=True)

    objects=ValorizacionManager()
    
    def save(self, *args, **kwargs):
        if self.id_valorizacion == "N/A":
            current_year = timezone.now().year
            last_instance = Valorizacion.objects.filter(id_valorizacion__startswith=f'VL-{current_year}-').order_by('-id_valorizacion').first()
            if last_instance:
                last_id = int(last_instance.id_valorizacion.split('-')[-1])
                next_id = last_id + 1
            else:
                next_id = 1
            self.id_valorizacion = f'VL-{current_year}-{str(next_id).zfill(8)}'

        # Generar la ruta de subida del archivo
        # print(self.presupuesto.field.has_changed(self.presupuesto, self.presupuesto.name))

        if bool(self.presupuesto) and not os.path.exists(self.presupuesto.path):
            ruta_archivo = f'{self.trabajo}/{self.id_valorizacion}/{self.presupuesto.name}'
            self.presupuesto.name = ruta_archivo
        
        
        super(Valorizacion, self).save(*args, **kwargs)

    def __str__(self):
        return self.id_valorizacion
