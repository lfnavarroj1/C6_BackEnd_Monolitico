from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models.trabajo import Trabajo
from .models.valorizacion import (
    Valorizacion, 
    Nodo,
    EtlBudget,
    NodoMDO, 
    NodoMAT
    )
from .models.trazabilidad import Trazabilidad
from .models.odm import Odm 
from .models.lcl import Lcl
from .models.programacion import Programacion
from .models.maniobra import Maniobra
from .models.soportes_iniciales import SoportesIniciales
from .models.libreto import Libreto
from .models.nodo_seguimiento import NodoSeguimiento


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


# NODO
class NodoResource( resources.ModelResource ):
    class Meta:
        model = Nodo
        fields = (
            "id_nodo",
            "valorizacion",
            "nodo",
            "latitud_inicial",
            "longitud_inicial",
            "latitud_final",
            "longitud_final",
            "punto_fisico_inicial",
            "punto_fisico_final",
            "norma_codensa_punto_inicial",
            "norma_codensa_punto_final",
            "tipo_nodo",
            "tipo_instalacion",
            "nivel_tension",
            "tramo",
            "cod_seccion",
            "cod_defecto",
            "valor_mano_obra",
            "valor_materiales",
            "id_mare",
        )

@admin.register( Nodo )
class NodoAdmin( ImportExportModelAdmin ):
    resource_class = NodoResource
    list_display = (
        "id_nodo",
        "valorizacion",
        "nodo",
        "tipo_nodo",
        "tipo_instalacion",
        "nivel_tension",
    )

# EtlBuget
class EtlBudgetResource( resources.ModelResource ):
    class Meta:
        model = EtlBudget
        fields = (
            "nodo",
            "instalacion_retiro",
            "codigo",
            "cantidad",
            "mat_mdo",
            "aportacion",
        )

@admin.register( EtlBudget )
class EtlBudgetAdmin( ImportExportModelAdmin ):
    resource_class = EtlBudgetResource
    list_display = (
        "nodo",
        "instalacion_retiro",
        "codigo",
        "cantidad",
        "mat_mdo",
        "aportacion",
    )

    search_fields=(
        'codigo',
    )
    list_filter=(
        'nodo', 'codigo',
    )


# NodoMDO
class NodoMDOResource(resources.ModelResource):
    class Meta:
        model=NodoMDO
        fields=(
            "nodo",
            "tipo_trabajo_mdo",
            "codigo_mdo",
            "cantidad_replanteada",
        )

@admin.register(NodoMDO)
class NodoMDOAdmin(ImportExportModelAdmin):
    resource_class=NodoMDOResource
    list_display=(
            "nodo",
            "tipo_trabajo_mdo",
            "codigo_mdo",
            "cantidad_replanteada",
    )

# NodoMAT
class NodoMATResource(resources.ModelResource):
    class Meta:
        model=NodoMAT
        fields=(
            "nodo",
            "tipo_trabajo_mat",
            "codigo_mat",
            "cantidad_replanteada",
        )

@admin.register(NodoMAT)
class NodoMATAdmin(ImportExportModelAdmin):
    resource_class=NodoMATResource
    list_display=(
            "nodo",
            "tipo_trabajo_mat",
            "codigo_mat",
            "cantidad_replanteada",
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
    list_display = (
        'id_programcion',
        'fecha_ejecucion',
        # 'cuadrilla',
        # 'lcl',
        'alcance',
        'estado',
    )

# NODOS SEGUIMIENTO
class NodoSeguimientoResource(resources.ModelResource):
    class Meta:
        model=Programacion
        fields=(
            'nodo',
            'programacion',
            'programado',
            'ejecutado',
            'facturado',
        )

@admin.register(NodoSeguimiento)
class NodoSeguimientoAdmin(ImportExportModelAdmin):
    resource_class=NodoSeguimientoResource
    list_display=(
            'nodo',
            'programacion',
            'programado',
            'ejecutado',
            'facturado',
    )



# MANIOBRA
class ManiobraResource(resources.ModelResource):
    class Meta:
        model=Maniobra
        fields=(
            'maniobra',
            'programaciones',
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
        'maniobra',
        # 'programacion',
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