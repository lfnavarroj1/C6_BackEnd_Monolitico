from django.db import models
from django.utils import timezone

from ...work_management.models.trabajo import Trabajo
from ...static_data.models.nivel_tension import NivelTension
from ..managers.valorizacion_manager import ValorizacionManager

import os

class Valorizacion( models.Model ):

    ESTADO_CHOICES = (
        ('0', 'Revisión'),
        ('1', 'Rechazado'),
        ('2', 'Aprobado'),
        ('3', 'Aprobado con modificación'),
        ('4', 'Anulado'),
    )

    id_valorizacion = models.CharField(primary_key=True, max_length=23, unique=True, default="N/A", editable=False)
    trabajo = models.ForeignKey(Trabajo, on_delete=models.PROTECT)
    monto_mano_obra = models.FloatField()
    monto_materiales = models.FloatField()
    fecha_valorizacion = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    estado = models.CharField(max_length=1,choices=ESTADO_CHOICES)
    nivel_tension = models.ForeignKey(NivelTension, on_delete=models.PROTECT)
    presupuesto = models.FileField(upload_to='presupuesto',blank=True, null=True)

    objects = ValorizacionManager()
    
    def save( self, *args, **kwargs ):
        if self.id_valorizacion == "N/A":
            current_year = timezone.now().year
            last_instance = Valorizacion.objects.filter(id_valorizacion__startswith=f'VL-{current_year}-').order_by('-id_valorizacion').first()
            if last_instance:
                last_id = int(last_instance.id_valorizacion.split('-')[-1])
                next_id = last_id + 1
            else:
                next_id = 1
            self.id_valorizacion = f'VL-{current_year}-{str(next_id).zfill(8)}'

        # Generar la ruta de subida del archivo
        # print(self.presupuesto.field.has_changed(self.presupuesto, self.presupuesto.name))

        if bool(self.presupuesto) and not os.path.exists(self.presupuesto.path):
            ruta_archivo = f'{self.trabajo}/{self.id_valorizacion}/{self.presupuesto.name}'
            self.presupuesto.name = ruta_archivo

        
        super(Valorizacion, self).save(*args, **kwargs)

    def __str__(self):
        return self.id_valorizacion


class Nodo( models.Model ):
    TIPONODO = (
        ("0" , "Nodo red"),
        ("1" , "Tramo red"),
        ("2" , "Equipo"),
        ("3" , "Transformador"),
        ("4" , "Cámara subterránea"),
        ("5" , "Tramo canalización"),
        ("6" , "Ramming"),
        ("7" , "Cercha"),
    )

    TIPOINSTALACION = (
        ("0" , "Aéreo"),
        ("1" , "Subterráneo"),
    )

    id_nodo = models.CharField( primary_key = True, max_length = 23, unique=True, default="N/A", editable=False )
    valorizacion = models.ForeignKey( Valorizacion, on_delete=models.PROTECT )
    nodo = models.CharField( max_length = 20 )
    latitud_inicial = models.CharField( max_length = 11 )
    longitud_inicial = models.CharField( max_length = 11 )
    latitud_final = models.CharField( max_length = 11, null=True, blank=True )
    longitud_final = models.CharField( max_length = 11, null=True, blank=True )
    punto_fisico_final = models.CharField( max_length = 10, null=True, blank=True )
    punto_fisico_inicial = models.CharField( max_length = 10, null=True, blank=True )
    norma_codensa_punto_inicial = models.CharField( max_length = 10, null=True, blank=True )
    norma_codensa_punto_final = models.CharField( max_length = 10, null=True, blank=True )
    tipo_nodo = models.CharField( max_length = 1,choices=TIPONODO, null=True, blank=True )
    tipo_instalacion = models.CharField( max_length = 1,choices=TIPOINSTALACION, null=True, blank=True )
    nivel_tension = models.ForeignKey( NivelTension, on_delete=models.PROTECT, null=True, blank=True )
    tramo = models.CharField( max_length = 200, null=True, blank=True )
    cod_seccion = models.CharField( max_length = 125, null=True, blank=True )
    cod_defecto = models.CharField( max_length = 250, null=True, blank=True )
    valor_mano_obra = models.FloatField( null=True, blank=True )
    valor_materiales = models.FloatField( null=True, blank=True )
    id_mare = models.CharField( max_length = 20, null=True, blank=True )

    class Meta:
        unique_together = ('valorizacion', 'nodo')

    def save(self, *args, **kwargs):
        if self.id_nodo == "N/A":
            current_year = timezone.now().year
            last_instance = Nodo.objects.filter(id_nodo__startswith=f'ND-{current_year}-').order_by('-id_nodo').first()
            if last_instance:
                last_id = int(last_instance.id_nodo.split('-')[-1])
                next_id = last_id + 1
            else:
                next_id = 1
            self.id_nodo = f'ND-{current_year}-{str(next_id).zfill(8)}'
        
        
        super(Nodo, self).save(*args, **kwargs)

    def __str__(self):
        return self.id_nodo


class NodoMDO( models.Model ):
    TIPOTRABAJOMDO = (
        ("0", "Retiro"),
        ("1", "Instlación"),
        ("2", "Traslado"),
        ("3", "Otro"),
    )
    nodo = models.ForeignKey( Nodo, on_delete = models.PROTECT )
    tipo_trabajo_mdo = models.CharField( max_length = 1,choices = TIPOTRABAJOMDO )
    codigo_mdo = models.CharField( max_length = 8 )
    cantidad_replanteada = models.FloatField(null=True, blank=True)
    cantidad_ejecutada = models.FloatField(null=True, blank=True)
    cantidad_facturada = models.FloatField(null=True, blank=True)


class NodoMAT( models.Model ):
    TIPOTRABAJOMAT = (
        ("0", "Instalación nuevo"),
        ("1", "Instalación reutilizable"),
        ("2", "Retiro chatarra"),
        ("3", "Retirado reutilizable"),
        ("4", "Material de aportacion"),
        ("5", "Hurto"),
        ("6", "No se pudo sacar el material"),
    )
    nodo = models.ForeignKey(Nodo, on_delete = models.PROTECT)
    tipo_trabajo_mat = models.CharField(max_length = 1,choices = TIPOTRABAJOMAT)
    codigo_mat = models.CharField(max_length = 8)
    cantidad_replanteada = models.FloatField(null=True, blank=True)
    cantidad_ejecutada = models.FloatField(null=True, blank=True)
    cantidad_facturada = models.FloatField(null=True, blank=True)
    aportacion = models.BooleanField( null = True, blank = True )


class EtlBudget( models.Model ):
    INSTALACION_RETIRO = (
        ( "0", "Retiro" ),
        ( "1", "Instlación" ),
        ( "2", "Traslado" ),
        ( "3", "Otro" ),
    )
    MATERIAL_MANO_OBRA = (
        ( "0", "Material" ),
        ( "1", "Mano de obra" ),
    )
    nodo = models.ForeignKey( Nodo, on_delete = models.PROTECT )
    instalacion_retiro = models.CharField( max_length = 1, choices = INSTALACION_RETIRO )
    codigo = models.CharField( max_length = 8 )
    cantidad = models.FloatField()
    mat_mdo = models.CharField( max_length = 1, choices = MATERIAL_MANO_OBRA )
    precio = models.FloatField( null=True, blank=True )
    aportacion = models.BooleanField()

    class Meta:
        unique_together = ('nodo', 'codigo')