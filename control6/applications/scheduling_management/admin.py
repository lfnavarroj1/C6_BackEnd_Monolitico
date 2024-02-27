from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models.programacion import Programacion




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

