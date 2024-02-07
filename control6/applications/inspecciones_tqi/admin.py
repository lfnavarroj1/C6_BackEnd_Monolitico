from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import PdlTqi, Asignaciones, MetasTQI, MetasInspectores, Maniobras

# Register your models here.

# PDL-TQI
class PdlTqiResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('codigo',)
        model=PdlTqi
        fields=(
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
        )

@admin.register(PdlTqi)
class PdlTqiAdmin(ImportExportModelAdmin):
    resource_class=PdlTqiResource
    list_display=(
            'codigo',
            'tipo',
            'descripcion',
            'estado_stweb',
            'fecha_inicio',
            'fecha_fin',
    )


# ASIGNACIONES
class AsignacionesResource(resources.ModelResource):
    class Meta:
        # import_id_fields = ('id_asignacion',)
        model = Asignaciones
        fields=(
            'id_asignacion',
            'pdl_tqi',
            'cedula_inspector',
            'estado_stweb',
            'cedula_responsable_asignacion',
            'fecha_asignacion',
            'ejecutado',
        )

@admin.register(Asignaciones)
class AsignacionesAdmin(ImportExportModelAdmin):
    resource_class=AsignacionesResource
    list_display=(
        'id_asignacion',
        'pdl_tqi',
        'cedula_inspector',
        'estado_stweb',
        'cedula_responsable_asignacion',
        'fecha_asignacion',
        'ejecutado',
    )


# METAS TQI
class MetasTQIResource(resources.ModelResource):
    class Meta:
        # import_id_fields = ('codigo',)
        model = MetasTQI
        fields = (
            'unidad_territorial',
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
    list_display=(
        'unidad_territorial',
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


    # MANIOBRAS
class ManiobrasResource(resources.ModelResource):
    class Meta:
        # import_id_fields = ('codigo',)
        model = Maniobras
        fields = (
            'codigo',
            'tipo',
            'fecha_trabajo_inicio',
            'hora_trabajo_inicio',
            'fecha_trabajo_fin',
        )

@admin.register(Maniobras)
class MetasInspectoresAdmin(ImportExportModelAdmin):
    resource_class = ManiobrasResource
    list_display = (
        'codigo',
        'tipo',
        'fecha_trabajo_inicio',
        'hora_trabajo_inicio',
        'fecha_trabajo_fin',
    )