from django.db import models
from django.utils import timezone
from .managers import TrabajoManager
from ..static_data.models.proceso import Proceso
from ..static_data.models.ruta_proceso import RutaProceso
from ..static_data.models.estructura_presupuestal import EstructuraPresupuestal
from ..static_data.models.unidad_territorial import UnidadTerritorial
from ..static_data.models.municipio import Municipio
from ..static_data.models.vereda import Vereda
from ..static_data.models.subestacion import Subestacion
from ..static_data.models.circuito import Circuito
from ..static_data.models.contrato import Contrato
from datetime import datetime

class Trabajo(models.Model):

    ESTADO_MARE = (
        ('0', 'ABIERTO'),
        ('1', 'YA NO ESTÁ PRESENTE'),
        ('2', 'ANULADO PLAN DE INVERSIÓN'),
        ('3', 'EJECUTADO')
    )

    ESTADO_PMS = (
        ("0", "Por Valorizar"),
        ("1", "Enviado a territorio"),
        ("2", "Valorizado"),
        ("3", "ODM Asignadas"),
        ("4", "PDL Programado"),
        ("5", "Trabajos finalizados"),
        ("6", "Negar solicitud"),
    )

    id_control = models.CharField(primary_key=True, max_length=20, unique=True, default="N/A", editable=False)
    pms_quotation = models.CharField(max_length=50, null=True, blank=True)
    pms_need = models.CharField(max_length=50, null=True, blank=True)
    proceso = models.ForeignKey(Proceso,on_delete=models.PROTECT) # R1
    ruta_proceso = models.ForeignKey(RutaProceso, on_delete=models.PROTECT)
    caso_radicado = models.CharField(max_length=180, null=True, blank=True)
    alcance = models.TextField()
    estructura_presupuestal = models.ForeignKey(EstructuraPresupuestal, on_delete=models.PROTECT, null=True, blank=True)
    priorizacion = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    unidad_territorial=models.ForeignKey(UnidadTerritorial, on_delete=models.PROTECT)
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT)
    vereda = models.ForeignKey(Vereda, on_delete=models.PROTECT)
    direccion = models.CharField(max_length=180)
    subestacion = models.ForeignKey(Subestacion, on_delete=models.PROTECT)
    circuito = models.ForeignKey(Circuito, on_delete=models.PROTECT)
    equipo_referencia = models.CharField(max_length=25, null=True, blank=True)
    carga_solicitada = models.CharField(max_length=25, null=True, blank=True)
    contrato = models.ForeignKey(Contrato, on_delete=models.PROTECT)
    ticket = models.CharField(max_length=50, null=True, blank=True)
    cantidad = models.IntegerField()
    estado_mare = models.CharField(max_length = 1,choices=ESTADO_MARE, null=True, blank=True)
    estado_pms = models.CharField(max_length = 1,choices=ESTADO_PMS, null=True, blank=True)
    anio_meta = models.PositiveIntegerField(null=True, blank=True)
    mes_meta = models.PositiveSmallIntegerField(null=True, blank=True)

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

        if isinstance(self.priorizacion, str):
            self.anio_meta = datetime.strptime(self.priorizacion, "%Y-%m-%d").year
            self.mes_meta = datetime.strptime(self.priorizacion, "%Y-%m-%d").month
        else:
            self.anio_meta = self.priorizacion.year
            self.anio_meta = self.priorizacion.month
        

        super(Trabajo, self).save(*args, **kwargs)
        return self
    
    def __str__(self):
        return self.id_control


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
