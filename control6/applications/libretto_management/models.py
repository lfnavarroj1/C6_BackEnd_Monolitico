from django.db import models
from django.utils import timezone
from ..scheduling_management.models import Programacion
from ..lcl_management.models import Lcl
from ..work_management.models import Trabajo
from ..users.models import User
from .manager import LibretoManager

import os

# Create your models here.

class Libreto(models.Model):
    ESTADO_LIBRETO=(
        ('0','PLANILLAS - CONCILIACIÓN'),
        ('1','PLANILLAS - RECHAZADAS'),
        ('2','PLANILLAS - FIRMADAS'),
        ('3','LIBRETO CARGADO EN SCM'),
        ('4','LIBRETO DEVULETO'),
        ('5','LIBRETO LIBERADO TECNICAMENTE'),
        ('6','LIBRETO LIBERADO CONTABLEMENTE'),
        ('7','LIBRETO CONFORMADO'),
    )
    id_libreto=models.CharField(primary_key=True, max_length=23, unique=True, default="N/A", editable=False)
    programacion=models.ForeignKey(Programacion, on_delete=models.PROTECT)
    lcl=models.ForeignKey(Lcl, on_delete=models.PROTECT, blank=True, null=True)
    numero_libreto = models.CharField(max_length=3)
    valor_mod = models.FloatField()
    valor_mat = models.FloatField()
    observacion=models.TextField()
    planillas_conciliacion=models.FileField(upload_to='planillas-conciliacion',blank=True, null=True)
    planillas_firmadas=models.FileField(upload_to='planillas-firmadas',blank=True, null=True)
    estado_libreto = models.CharField(max_length=1, choices=ESTADO_LIBRETO)
    es_ultimo_libreto=models.BooleanField()
    trabajo=models.ForeignKey(Trabajo, on_delete=models.PROTECT) 

    objects=LibretoManager()

    def save(self, *args, **kwargs):
        if self.id_libreto == "N/A":
            current_year = timezone.now().year
            last_instance = Libreto.objects.filter(id_libreto__startswith=f'LB-{current_year}-').order_by('-id_libreto').first()
            if last_instance:
                last_id = int(last_instance.id_libreto.split('-')[-1])
                next_id = last_id + 1
            else:
                next_id = 1
            self.id_libreto = f'LB-{current_year}-{str(next_id).zfill(8)}'


        # Generar la ruta de subida del archivo
        if bool(self.planillas_conciliacion) and not os.path.exists(self.planillas_conciliacion.path):
            ruta_archivo1 = f'{self.trabajo}/{self.id_libreto}/{self.planillas_conciliacion.name}'
            self.planillas_conciliacion.name = ruta_archivo1


        if bool(self.planillas_firmadas) and not os.path.exists(self.planillas_firmadas.path):
            ruta_archivo2 = f'{self.trabajo}/{self.id_libreto}/{self.planillas_firmadas.name}'
            self.planillas_firmadas.name = ruta_archivo2

        super(Libreto, self).save(*args, **kwargs)

    def __str__(self):
        return self.id_libreto