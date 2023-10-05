from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models.trabajo import Trabajo
from .models.valorizacion import Valorizacion
from .models.trazabilidad import Trazabilidad
from .models.odm import Odm 
from .models.lcl import Lcl
from .models.programacion import Programacion
from .models.maniobra import Maniobra
from .models.ejecutado import Ejecutado


# TRABAJO
class TrabajoResource(resources.ModelResource):
    class Meta:
        model=Trabajo
        fields=(
            'id_control',
            'pms_quotation',
            'pms_need',
            'proceso',
            'caso_radicado',
            'direccion',
            'alcance',
            'priorizacion',
            'estructura_presupuestal',
            'municipio',
            'vereda',
            'subestacion',
            'circuito',
            'estado_trabajo',
            'contrato',
        )

@admin.register(Trabajo)
class TrabajoAdmin(ImportExportModelAdmin):
    resource_class=TrabajoResource
    list_display=(
        'id_control',
        'pms_quotation',
        'pms_need',
        'proceso',
        'caso_radicado',
        'estado_trabajo',
    )
    search_fields=(
        'pms_quotation',
    )
    list_filter=(
        'estado_trabajo', 'proceso',
    )


# TRAZABILIDAD
class TrazabilidadResource(resources.ModelResource):
    class Meta:
        model=Trazabilidad
        fields=(
            'trabajo',
            'usuario',
            'fecha_trazabilidad',
            'comentario_trazabilidad',
        )

@admin.register(Trazabilidad)
class TrazabilidadAdmin(ImportExportModelAdmin):
    resource_class=TrazabilidadResource
    list_display=(
        'trabajo',
        'usuario',
        'fecha_trazabilidad',
        'comentario_trazabilidad',
    )


# VALORIZACIÓN
class ValorizacionResource(resources.ModelResource):
    class Meta:
        model=Valorizacion
        fields=(
            'id_valorizacion',
            'trabajo',
            'monto_mano_obra',
            'monto_materiales',
            'estado',
            'nivel_tension',
            'presupuesto',
            'estado_trabajo',
        )

@admin.register(Valorizacion)
class ValorizacionAdmin(ImportExportModelAdmin):
    resource_class=ValorizacionResource
    list_display=(
        'id_valorizacion',
        'trabajo',
        'monto_mano_obra',
        'monto_materiales',
        'estado',
        'nivel_tension',
        'presupuesto',
        'estado_trabajo',
    )


# ODM
class OdmResource(resources.ModelResource):
    class Meta:
        model=Odm
        fields=(
            'odm',
            'valorizacion',
            'agp',
            'protocolo',
            'solicitud',
            'tiene_lcl',
        )

@admin.register(Odm)
class OdmAdmin(ImportExportModelAdmin):
    resource_class=OdmResource
    list_display=(
        'odm',
        'valorizacion',
        'agp',
        'protocolo',
        'solicitud',
        'tiene_lcl',
    )


# LCL
class LclResource(resources.ModelResource):
    class Meta:
        model=Lcl
        fields=(
            'numero_lcl',
            'estado_lcl',
            'indicador_impuesto',
            'valor_mano_obra',
            'valor_materiales',
            'responsable_scm',
            'texto_scm',
            'alcance',
            'odms',
        )

@admin.register(Lcl)
class LclAdmin(ImportExportModelAdmin):
    resource_class=LclResource
    list_display=(
        'numero_lcl',
        'estado_lcl',
        'indicador_impuesto',
        'valor_mano_obra',
        'valor_materiales',
        'responsable_scm',
        'texto_scm',
        'alcance',
        #'odms',
    )


# PROGRAMACION
class ProgramacionResource(resources.ModelResource):
    class Meta:
        model=Programacion
        fields=(
            'id_programcion',
            'fecha_ejecucion',
            'cuadrilla',
            'lcl',
            'alcance',
            'estado',
        )

@admin.register(Programacion)
class ProgramacionAdmin(ImportExportModelAdmin):
    resource_class=ProgramacionResource
    list_display=(
        'id_programcion',
        'fecha_ejecucion',
        'cuadrilla',
        'lcl',
        'alcance',
        'estado',
    )


# MANIOBRA
class ManiobraResource(resources.ModelResource):
    class Meta:
        model=Maniobra
        fields=(
            'mabiobra',
            'programacion',
            'tipo_maniobra',
            'alcance',
            'fecha_inicio',
            'fecha_fin',
            'estado_maniobra',
        )

@admin.register(Maniobra)
class ManiobraAdmin(ImportExportModelAdmin):
    resource_class=ManiobraResource
    list_display=(
        'mabiobra',
        'programacion',
        'tipo_maniobra',
        'alcance',
        'fecha_inicio',
        'fecha_fin',
        'estado_maniobra',
    )


# EJECUTADO
class EjecutadoResource(resources.ModelResource):
    class Meta:
        model=Ejecutado
        fields=(
            'id_ejecucutado',
            'maniobras',
            'monto_mano_obra',
            'monto_materiales',
            'estado',
            'soporte',
        )

@admin.register(Ejecutado)
class EjecutadoAdmin(ImportExportModelAdmin):
    resource_class=EjecutadoResource
    list_display=(
        'id_ejecucutado',
        'maniobras',
        'monto_mano_obra',
        'monto_materiales',
        'estado',
        'soporte',
    )

