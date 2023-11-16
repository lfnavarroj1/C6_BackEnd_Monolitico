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

    )
    id_hora_extra = models.CharField(primary_key=True, max_length=25, unique=True, default="N/A", editable=False)
    usuario= models.ForeignKey(User, on_delete=models.PROTECT)
    fecha = models.DateField(auto_now=False, auto_now_add=False)
    hora_entrada=models.TimeField()
    hora_salida=models.TimeField()
    observacion=models.TextField()
    estado=models.CharField(max_length=1,choices=ESTADO_HE)


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