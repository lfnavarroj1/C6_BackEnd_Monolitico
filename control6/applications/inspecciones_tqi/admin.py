from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import ManiobrasTqi, MetasTQI, MetasInspectores

class ManiobrasTqiResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('codigo',)
        model = ManiobrasTqi
        fields = (
            'codigo',
            'tipo',
            'descripcion',
            'estado_stweb',
            'fecha_inicio',
            'fecha_fin',
            'hora_inicio',
            'hora_fin',
            'circuito',
            'unidad_territorial',
            'unidad',
            'causal',
            'pdl_asociado',
            'fecha_actualizacion',
            'contrato',
            'municipio',
            'vereda_localidad',
            'direccion',
            'estado_tqi',
            'criticidad_maniobra',
            'cuadrilla_responsable',
            'telefono_cuadrilla_responsable',
            'inspector_asingado',
            'inspeccion_ejecutada',
        )

@admin.register(ManiobrasTqi)
class PdlTqiAdmin(ImportExportModelAdmin):
    resource_class = ManiobrasTqiResource
    list_display = (
        'codigo',
        'tipo',
        'descripcion',
        'estado_stweb',
        'fecha_inicio',
        'fecha_fin',
    )



# METAS TQI
class MetasTQIResource(resources.ModelResource):
    class Meta:
        # import_id_fields = ('codigo',)
        model = MetasTQI
        fields = (
            'id',
            'contrato',
            'anio',
            'mes',
            'cantidad_meta',
            'cantidad_programada',
            'cantidad_ejecutada',
            'fecha_actualizacion',
            'responsable_actualizacion',
        )

@admin.register(MetasTQI)
class MetasTQIAdmin(ImportExportModelAdmin):
    resource_class=MetasTQIResource
    list_display = (
        'contrato',
        'anio',
        'mes',
        'cantidad_meta',
        'cantidad_programada',
        'cantidad_ejecutada',
        'fecha_actualizacion',
        'responsable_actualizacion',
    )


# META INSPECTORES TQI
class MetasInspectoresResource(resources.ModelResource):
    class Meta:
        # import_id_fields = ('codigo',)
        model = MetasInspectores
        fields=(
            'id',
            'inspector',
            'anio',
            'mes',
            'cantidad_meta',
            'cantidad_programada',
            'cantidad_ejecutada',
            'fecha_actualizacion',
            'responsable_actualizacion',
        )

@admin.register(MetasInspectores)
class MetasInspectoresAdmin(ImportExportModelAdmin):
    resource_class = MetasInspectoresResource
    list_display = (
        'inspector',
        'anio',
        'mes',
        'cantidad_meta',
        'cantidad_programada',
        'cantidad_ejecutada',
        'fecha_actualizacion',
        'responsable_actualizacion',
    )