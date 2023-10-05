from django.db import models
from .maniobra import Maniobra
from django.utils import timezone
# Create your models here.

class Ejecutado(models.Model):

    ESTADO_CHOICES=(
        ('0','Soportes EECC'),
        ('1','Soportes Enel'),
        ('2','Planillas firmadas'),
        ('3','Rechazdo'),
    )
    id_ejecucutado=models.CharField(primary_key=True, max_length=23, unique=True, default="N/A", editable=False)
    maniobras=models.ForeignKey(Maniobra, on_delete=models.PROTECT)
    monto_mano_obra=models.FloatField()
    monto_materiales=models.FloatField()
    estado = models.CharField(max_length=1,choices=ESTADO_CHOICES)
    soporte=models.FileField(upload_to=None, max_length=100)

    def save(self, *args, **kwargs):
        if self.id_ejecucutado == "N/A":
            current_year = timezone.now().year
            last_instance = Ejecutado.objects.filter(id_ejecucutado__startswith=f'EX-{current_year}-').order_by('-id_ejecucutado').first()
            if last_instance:
                last_id = int(last_instance.id_ejecucutado.split('-')[-1])
                next_id = last_id + 1
            else:
                next_id = 1
            self.id_ejecucutado = f'EX-{current_year}-{str(next_id).zfill(2)}'
        super(Ejecutado, self).save(*args, **kwargs)

    def __str__(self):
        return self.id_ejecucutado
