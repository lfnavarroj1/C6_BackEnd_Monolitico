from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from ..traceability_management.models import TrazabilidadTrabajo

class TrazabilidadTrabajoResource(resources.ModelResource):
    class Meta:
        model = TrazabilidadTrabajo
        fields = (
            'trabajo__id_control',
            'usuario',
            'fecha_trazabilidad',
            'comentario_trazabilidad',
        )

@admin.register(TrazabilidadTrabajo)
class TrazabilidadAdmin(ImportExportModelAdmin):
    resource_class = TrazabilidadTrabajoResource
    list_display = (
        'trabajo',
        'usuario',
        'fecha_trazabilidad',
        'comentario_trazabilidad',
    )



