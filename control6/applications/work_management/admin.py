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
from .models.soportes_iniciales import SoportesIniciales
from .models.libreto import Libreto


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
            'ruta_proceso',
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
        'ruta_proceso',
    )
    search_fields=(
        'pms_quotation',
    )
    list_filter=(
        'ruta_proceso', 'proceso',
    )


# TRAZABILIDAD
class TrazabilidadResource(resources.ModelResource):
    class Meta:
        model=Trazabilidad
        fields=(
            'trabajo__id_control',
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
    )


# LCL
class LclResource(resources.ModelResource):
    class Meta:
        model=Lcl
        fields=(
            'lcl',
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
        'lcl',
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

# SOPORTES INICIALES
class SoportesInicialesResource(resources.ModelResource):
    class Meta:
        model=SoportesIniciales
        fields=(
            'id_soporte',
            'trabajo',
            'nombre',
            'descripcion',
            'archivo',
        )

@admin.register(SoportesIniciales)
class SoportesInicialesAdmin(ImportExportModelAdmin):
    resource_class=SoportesInicialesResource
    list_display=(
        'id_soporte',
        'trabajo',
        'nombre',
        'descripcion',
        'archivo',
    )


# LIBRETOS
class LibretoResource(resources.ModelResource):
    class Meta:
        model=Libreto
        fields=(
            "id_libreto",
            "programacion",
            "numero_libreto",
            "valor_mod",
            "valor_mat",
            "observacion",
            "planillas_conciliacion",
            "planillas_firmadas",
            "estado_libreto",
            "es_ultimo_libreto",
            "trabajo",
        )

@admin.register(Libreto)
class LibretoAdmin(ImportExportModelAdmin):
    resource_class=LibretoResource
    list_display=(
            "id_libreto",
            "programacion",
            "numero_libreto",
            "valor_mod",
            "valor_mat",
            "observacion",
            "planillas_conciliacion",
            "planillas_firmadas",
            "estado_libreto",
            "es_ultimo_libreto",
            "trabajo",
    )