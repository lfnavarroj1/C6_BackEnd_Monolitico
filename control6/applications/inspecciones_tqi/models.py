from django.db import models
from ..users.models import User
from ..static_data.models.unidad_territorial import UnidadTerritorial
from ..static_data.models.subestacion import Subestacion
from ..static_data.models.circuito import Circuito
from ..static_data.models.contrato import Contrato
from ..static_data.models.municipio import Municipio
from ..static_data.models.vereda import Vereda
from .managers import ManiobrasTQIManager, MetasInspectoresManager
from datetime import datetime


class ManiobrasTqi(models.Model):

    ESTADO_TQI = (
        ("0", "SIN ASIGNACION"),
        ("1", "PROGRAMADO INTERVENTORIA"),
        ("2", "ASIGNADO PERSONAL PROPIO"),
    )

    TIPO_MANIOBRA = (
        ("0", "Trabajos en Tensión (ID)"),
        ("1", "Trabajos en Tensión (PSTL)"),
        ("2", "Trabajos sin Tensión (PDL)"),
        ("3", "Verificación y prueba (VyP)"),
        ("4", "Incidencia (Ticket)"),
        ("5", "Trabajo en proximidad (PI)"),
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
    unidad_territorial = models.ForeignKey(UnidadTerritorial, null=True, blank=True, on_delete=models.PROTECT, related_name="maniobra_unidad_territorial")
    subestacion = models.ForeignKey(Subestacion, null=True, blank=True, on_delete=models.PROTECT)
    circuito = models.ForeignKey(Circuito, null=True, blank=True, on_delete=models.PROTECT)
    unidad_ejecutora = models.ForeignKey(UnidadTerritorial, null=True, blank=True, on_delete=models.PROTECT, related_name="maniobra_unidad_ejecutora")
    causal = models.CharField(max_length = 1,choices=TIPO_CAUSA)
    pdl_asociado = models.CharField(max_length=25, null=True, blank=True)
    fecha_actualizacion = models.DateTimeField(null=True, blank=True)
    contrato = models.ForeignKey(Contrato, null=True, blank=True, on_delete=models.PROTECT, related_name="maniobra_contrato")
    municipio = models.ForeignKey(Municipio, null=True, blank=True, on_delete=models.PROTECT, related_name="maniobra_municipio")
    vereda_localidad = models.ForeignKey(Vereda, null=True, blank=True, on_delete=models.PROTECT, related_name="maniobra_vereda_localidad")
    direccion = models.CharField(null=True, blank=True, max_length=200)
    estado_tqi = models.CharField(max_length = 1,choices=ESTADO_TQI)
    criticidad_maniobra = models.CharField(null=True, blank=True, max_length=200)
    cuadrilla_responsable = models.CharField(max_length=120, null=True, blank=True)
    telefono_cuadrilla_responsable = models.CharField(max_length=120, null=True, blank=True)
    inspector_asingado = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    anio = models.PositiveIntegerField(null=True, blank=True)
    mes = models.PositiveIntegerField(null=True, blank=True)
    inspeccion_ejecutada = models.BooleanField(null=True, blank=True)

    objects = ManiobrasTQIManager()

    def save(self, *args, **kwargs):
        if isinstance(self.fecha_fin, str):
            self.anio = datetime.strptime(self.fecha_fin, "%Y-%m-%d").year
            self.mes = datetime.strptime(self.fecha_fin, "%Y-%m-%d").month
        else:
            self.anio = self.fecha_fin.year
            self.mes = self.fecha_fin.month
        
        super(ManiobrasTqi, self).save(*args, **kwargs)
        return self
    
    def __str__(self):
        return self.codigo

    @classmethod
    def obtener_valor_estado_stweb(cls, etiqueta):
        for valor, etq in cls.ESTADO_STWEB:
            if etq == etiqueta:
                return valor
        return None
    
    @classmethod
    def obtener_valor_tipo_maniobra(cls, etiqueta):
        for valor, etq in cls.TIPO_MANIOBRA:
            if etq == etiqueta:
                return valor
        return None
    
    @classmethod
    def obtener_valor_tipo_causa(cls, etiqueta):
        for valor, etq in cls.TIPO_CAUSA:
            if etq == etiqueta:
                return valor
        return None


class MetasTQI(models.Model):
    contrato = models.ForeignKey(Contrato,on_delete=models.PROTECT, null=True, blank=True)
    anio = models.PositiveIntegerField()
    mes = models.PositiveIntegerField()
    cantidad_meta = models.PositiveIntegerField()
    cantidad_programada = models.PositiveIntegerField()
    cantidad_ejecutada = models.PositiveIntegerField()
    fecha_actualizacion = models.DateTimeField()
    responsable_actualizacion= models.CharField(max_length=11)


class MetasInspectores(models.Model):
    inspector = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    anio = models.CharField(max_length=200)
    mes = models.PositiveIntegerField()
    cantidad_meta = models.PositiveIntegerField()
    cantidad_programada = models.PositiveIntegerField()
    cantidad_ejecutada = models.PositiveIntegerField()
    fecha_actualizacion = models.DateTimeField()
    responsable_actualizacion= models.CharField(max_length=11)

    objects = MetasInspectoresManager()

