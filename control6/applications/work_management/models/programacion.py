from django.db import models
from django.utils import timezone

from .lcl import Lcl
from ..managers.programacion_manager import ProgramacionManager
from ...static_data.models.cuadrilla import Cuadrilla
from .trabajo import Trabajo

import os

class Programacion(models.Model):

    ESTADO_PROGRAMACION = (
        ('0', 'Sin maniobra'),
        ('1', 'Con maniobra no aprobada'),
        ('2', 'Con maniobra aprobada'),
        ('3', 'Ejecutada'),
        ('4', 'Ejecutada parcialmente'),
        ('5', 'Cancelada'),
    )

    # Lista de atributos de la programación
    id_programcion = models.CharField(
        primary_key=True, 
        max_length = 25, 
        unique = True, 
        default = "N/A", 
        editable = False
    )
    trabajo = models.ForeignKey(Trabajo, on_delete = models.PROTECT, null=True, blank=True)
    fecha_ejecucion = models.DateField(auto_now = False, auto_now_add = False)
    cuadrillas = models.ManyToManyField(Cuadrilla)
    lcls = models.ManyToManyField(Lcl)
    alcance = models.TextField()
    estado = models.CharField(max_length = 1, choices = ESTADO_PROGRAMACION)
    observacion  = models.TextField(blank = True, null = True)
    ticket = models.BooleanField(null = True, blank = True)
    pdl = models.BooleanField(null = True, blank = True)
    pi = models.BooleanField(null = True, blank = True)
    pstl = models.BooleanField(null = True, blank = True)
    vyp = models.BooleanField(null = True, blank = True)
    planeacion_segura = models.FileField(upload_to = 'programaciones', blank = True, null = True)
    
    objects = ProgramacionManager()

    def save(self, *args, **kwargs):
        if self.id_programcion == "N/A":
            current_year = timezone.now().year

            last_instance = Programacion.objects.filter(
                id_programcion__startswith=f'PR-{current_year}-'
            ).order_by( '-id_programcion' ).first()

            if last_instance:
                last_id = int( last_instance.id_programcion.split('-')[-1] )
                next_id = last_id + 1
            else:
                next_id = 1

            self.id_programcion = f'PR-{current_year}-{str(next_id).zfill(8)}'

        # Generar la ruta de subida del archivo
        if bool(self.planeacion_segura) and not os.path.exists(self.planeacion_segura.path):
            ruta_archivo = f'{self.trabajo}/{self.id_programcion}/{self.planeacion_segura.name}'

            # print(ruta_archivo)
            self.planeacion_segura.name = ruta_archivo

        super( Programacion, self ).save( *args, **kwargs )

    def __str__(self):
        return self.id_programcion