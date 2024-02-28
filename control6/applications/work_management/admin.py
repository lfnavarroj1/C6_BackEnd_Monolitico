from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Trabajo


class TrabajoResource(resources.ModelResource):
    class Meta:
        model = Trabajo
        fields = (
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
    resource_class = TrabajoResource
    list_display = (
        'id_control',
        'pms_quotation',
        'pms_need',
        'proceso',
        'caso_radicado',
        'ruta_proceso',
    )
    search_fields = (
        'pms_quotation',
    )
    list_filter = (
        'ruta_proceso', 'proceso',
    )


