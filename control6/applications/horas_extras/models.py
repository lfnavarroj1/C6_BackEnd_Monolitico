from django.db import models
from django.utils import timezone
from ..users.models import User
from .managers import HorasExtrasManager

# Create your models here.

class CalendarioFestivo(models.Model):
    id_festivo=models.CharField(primary_key=True, max_length=25)
    fecha=models.DateField(auto_now=False, auto_now_add=False)
    celebracion=models.CharField(max_length=300)


class HoraExtra(models.Model):
    ESTADO_HE=( # Independizar una tabla con los estados.
        ('0','Pendientes por aprobación'),
        ('1','Aprobadas'),
        ('2','Rechazadas'),

    )
    id_hora_extra = models.CharField(primary_key=True, max_length=25, unique=True, default="N/A", editable=False)
    usuario= models.ForeignKey(User, on_delete=models.PROTECT)
    fecha = models.DateField(auto_now=False, auto_now_add=False)
    hora_entrada=models.TimeField()
    hora_salida=models.TimeField()
    observacion=models.TextField()
    estado=models.CharField(max_length=1,choices=ESTADO_HE)
    cod_4185=models.FloatField(default=0.0)
    cod_4215=models.FloatField(default=0.0)
    cod_4225=models.FloatField(default=0.0)
    cod_4230=models.FloatField(default=0.0)
    cod_4235=models.FloatField(default=0.0)
    cod_4240=models.FloatField(default=0.0)
    cod_4245=models.FloatField(default=0.0)
    cod_4270=models.FloatField(default=0.0)
    cod_4275=models.FloatField(default=0.0)
    cod_4280=models.FloatField(default=0.0)
    cod_9050=models.FloatField(default=0.0)
    cod_9054=models.FloatField(default=0.0)

    objects=HorasExtrasManager()

    def save(self, *args, **kwargs):
        if self.id_hora_extra == "N/A":
            current_year = timezone.now().year
            last_instance = HoraExtra.objects.filter(id_hora_extra__startswith=f'HE-{current_year}-').order_by('-id_hora_extra').first()

            if last_instance:
                last_id = int(last_instance.id_hora_extra.split('-')[-1])
                next_id = last_id + 1
            else:
                next_id = 1

            self.id_hora_extra = f'HE-{current_year}-{str(next_id).zfill(8)}'

        super(HoraExtra, self).save(*args, **kwargs)

    def __str__(self):
        return self.id_hora_extra

class CodigoConcepto(models.Model):
    codigo_concepto=models.CharField(max_length=4, primary_key=True)
    descripcion=models.CharField(max_length=150)
    recargo=models.CharField(max_length=150)
    observacion=models.CharField(max_length=250)