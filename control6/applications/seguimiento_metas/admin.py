from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import QProcesos, PProcesos


# Register your models here.

class QProcesosResource( resources.ModelResource ):
    class Meta:
        # import_id_fields = ( 'codigo_material' )
        model = QProcesos
        fields = (
            'unidad_territorial',
            'proceso',
            'anio',
            'mes',
            'q_meta',
            'q_proceso',
            'q_ejecutada',
            'q_facturado',
        )

@admin.register(QProcesos)
class MaterialAdmin(ImportExportModelAdmin):
    resource_class = QProcesosResource
    list_display = (
        'unidad_territorial',
        'proceso',
        'anio',
        'mes',
        'q_meta',
        'q_proceso',
        'q_ejecutada',
        'q_facturado',
    )


class PProcesosResource( resources.ModelResource ):
    class Meta:
        # import_id_fields = ( 'codigo_material' )
        model = PProcesos
        fields = (
            'unidad_territorial',
            'proceso',
            'anio',
            'mes',
            'p_meta',
            'p_proceso',
            'p_ejecutada',
            'p_facturado',
        )

@admin.register( PProcesos )
class MaterialAdmin( ImportExportModelAdmin ):
    resource_class = PProcesosResource
    list_display = (
    'unidad_territorial',
    'proceso',
    'anio',
    'mes',
    'p_meta',
    'p_proceso',
    'p_ejecutada',
    'p_facturado',
    )