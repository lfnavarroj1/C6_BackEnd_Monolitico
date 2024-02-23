from django.db import models
from django.utils import timezone
from ...work_management.models.trabajo import Trabajo


class SoportesIniciales(models.Model):
    id_soporte = models.CharField(primary_key=True, max_length=23, unique=True, default="N/A", editable=False)
    trabajo = models.ForeignKey(Trabajo, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to='soportes_iniciales',blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.id_soporte == "N/A":
            current_year = timezone.now().year
            last_instance = SoportesIniciales.objects.filter(id_soporte__startswith=f'SP-{current_year}-').order_by('-id_soporte').first()
            if last_instance:
                last_id = int(last_instance.id_soporte.split('-')[-1])
                next_id = last_id + 1
            else:
                next_id = 1
            self.id_soporte = f'SP-{current_year}-{str(next_id).zfill(8)}'

        ruta_archivo = f'{self.trabajo}/{self.id_soporte}/{self.archivo.name}'

        self.archivo.name = ruta_archivo

        super(SoportesIniciales, self).save(*args, **kwargs)

    def __str__(self):
        return self.id_soporte
