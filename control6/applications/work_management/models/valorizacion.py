from django.db import models
from django.utils import timezone
# Create your models here.

class Valorizacion(models.Model):

    ESTADO_CHOICES=(
        ('0','Revisión'),
        ('1','Rechazado'),
        ('2','Aprobado'),
        ('3','Anulado'),
    )

    id_valorizacion=models.CharField(primary_key=True, max_length=23, unique=True, default="N/A", editable=False)
    trabajo = models.CharField(max_length=20)
    monto_mano_obra=models.FloatField()
    monto_materiales=models.FloatField()
    estado = models.CharField(max_length=1,choices=ESTADO_CHOICES)
    nivel_tension=models.CharField(max_length=8)
    presupuesto=models.FileField(upload_to='presupuesto',blank=True, null=True)
    estado_trabajo=models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if self.id_valorizacion == "N/A":
            current_year = timezone.now().year
            last_instance = Valorizacion.objects.filter(id_valorizacion__startswith=f'VL-{current_year}-').order_by('-id_valorizacion').first()
            if last_instance:
                last_id = int(last_instance.id_valorizacion.split('-')[-1])
                next_id = last_id + 1
            else:
                next_id = 1
            self.id_valorizacion = f'PR-{current_year}-{str(next_id).zfill(2)}'
        super(Valorizacion, self).save(*args, **kwargs)

    def __str__(self):
        return self.id_valorizacion
