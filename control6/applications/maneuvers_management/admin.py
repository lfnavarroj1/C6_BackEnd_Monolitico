from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from ..maneuvers_management.models import Maniobra

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
        'tipo_maniobra',
        'alcance',
        'fecha_inicio',
        'fecha_fin',
        'estado_maniobra',
    )

