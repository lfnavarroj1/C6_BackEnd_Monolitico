from django.db import models
from django.utils import timezone


class Maniobras(models.Model):
    codigo = models.CharField(primary_key=True, max_length=25, unique=True)
    tipo = models.CharField()
    fecha_trabajo_inicio = models.DateField()
    hora_trabajo_inicio = models.TimeField()#: "07:00:00",
    fecha_trabajo_fin = models.DateField()#: "2024-02-10",
    hora_trabajo_fin = models.TimeField()#: "08:30:00",
    fecha_programacion = models.DateField()#: "2024-02-01",
    estado = models.CharField(max_length=150)#: "Aprobado",
    pdl_asociado = models.CharField(max_length=25, null=True, blank=True)#: " ",
    circuito = models.CharField(max_length=50, null=True, blank=True)#: "GUALI [300016 - SALITRE]",
    causal = models.CharField(max_length=50, null=True, blank=True)#: "Programado",
    descripcion = models.TextField()#: "PCBS; EXCLUIBLE RESOLUCION 222;SE REQUIERE TRABAJOS DE MUESTREO Y/O MARCACION SOBRE EL CTO GUALI APERTURA Y CIERRRE DEL CD 39551TR1;ODM81183603;LCL6300344482",
    unidad_territorial = models.CharField(max_length=80, null=True, blank=True)#: "CAM",
    unidad_territorial_std = models.CharField(max_length=80, null=True, blank=True)#: "CAM",
    fecha_actualizacion = models.DateTimeField()#: "2024-02-02T07:08:01.243883",
    ubicacion = models.CharField(max_length=128, null=True, blank=True)#: "NVA AK 68 64 C 75",
    localidad_municipio = models.CharField(max_length=128, null=True, blank=True)#: "CD1A202 - ENGATIVA",
    nombre_responsable = models.CharField(max_length=255, null=True, blank=True)#: "JUAN CARLOS MARTINEZ ARENAS",
    unidad_responsable = models.CharField(max_length=255 ,null=True, blank=True)#: "CAM",
    telefono_reponsable = models.CharField(max_length=255, null=True, blank=True)#: "3233213656",
    firma = models.CharField(max_length=255, null=True, blank=True)#: "ROMERO MEJIA ALBA AYDE (CO53008438)",
    co = models.CharField(max_length=255, null=True, blank=True)#: "53008438"


class PdlTqi(models.Model):

    ESTADO_TQI = (
        ("0", "SIN ASIGNACION"),
        ("1", "PROGRAMADO INTERVENTORIA"),
        ("2", "ASIGNADO PERSONAL PROPIO"),
    )

    TIPO_MANIOBRA = (
        ("0", "Trabajos en Tensión (ID)"),
        ("1", "Trabajos en Tensión (PSTL)"),
        ("2", "Trabajos sin Tensión (PDL)"),
    )

    ESTADO_STWEB = (
        ("0", "Aprobado"),
        ("1", "En ejecución"),
    )

    TIPO_CAUSA = (
        ("0", "Emergencial"),
        ("1", "Programado"),
    )

    codigo = models.CharField(primary_key=True, max_length=15, unique=True)
    tipo = models.CharField(max_length = 1,choices=TIPO_MANIOBRA)
    descripcion = models.TextField()
    estado_stweb = models.CharField(max_length = 1,choices=ESTADO_STWEB)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    circuito = models.CharField(max_length=255)
    unidad_territorial = models.CharField()
    unidad = models.CharField()
    causal = models.CharField(max_length = 1,choices=TIPO_CAUSA)
    pdl_asociado = models.CharField(max_length=50, null=True, blank=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    contrato = models.CharField(max_length=25)
    municipio = models.CharField(null=True, blank=True)
    vereda_localidad = models.CharField(null=True, blank=True)
    direccion = models.CharField(null=True, blank=True)
    estado_tqi = models.CharField(max_length = 1,choices=ESTADO_TQI)
    criticidad_maniobra = models.CharField(null=True, blank=True)


  
class Asignaciones(models.Model):
     
    ESTADO_STWEB = (
        ("0", "Aprobado"),
        ("1", "En ejecución"),
    )

    id_asignacion = models.CharField(primary_key=True, max_length=20, unique=True, default="N/A", editable=False)
    pdl_tqi = models.ForeignKey(PdlTqi, on_delete=models.PROTECT)
    cedula_inspector = models.CharField(max_length=11)
    estado_stweb = models.CharField(max_length = 1,choices=ESTADO_STWEB)
    cedula_responsable_asignacion = models.CharField(max_length=11)
    fecha_asignacion = models.DateTimeField()
    ejecutado = models.BooleanField()

    def save(self, *args, **kwargs):
        if self.id_asignacion == "N/A":
            current_year = timezone.now().year
            last_instance = Asignaciones.objects.filter(id_asignacion__startswith=f'INSP-{current_year}-').order_by('-id_asignacion').first()

            if last_instance:
                last_id = int(last_instance.id_asignacion.split('-')[-1])
                next_id = last_id + 1
            else:
                next_id = 1

            self.id_asignacion = f'INSP-{current_year}-{str(next_id).zfill(6)}'

        super(Asignaciones, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return self.id_asignacion


class MetasTQI(models.Model):
    unidad_territorial = models.CharField()
    contrato = models.CharField()
    anio = models.PositiveIntegerField()
    mes = models.PositiveIntegerField()
    cantidad_meta = models.PositiveIntegerField()
    cantidad_programada = models.PositiveIntegerField()
    cantidad_ejecutada = models.PositiveIntegerField()
    fecha_actualizacion = models.DateTimeField()
    responsable_actualizacion= models.CharField(max_length=11)


class MetasInspectores(models.Model):
    inspector = models.CharField(max_length=11)
    anio = models.CharField()
    mes = models.PositiveIntegerField()
    cantidad_meta = models.PositiveIntegerField()
    cantidad_programada = models.PositiveIntegerField()
    cantidad_ejecutada = models.PositiveIntegerField()
    fecha_actualizacion = models.DateTimeField()
    responsable_actualizacion= models.CharField(max_length=11)

