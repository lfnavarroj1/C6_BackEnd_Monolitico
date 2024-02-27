from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models.trazabilidad import Trazabilidad


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



