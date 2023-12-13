from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Prestacion

# Register your models here.

# PRESTACIONES
class PrestacionResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('codigo_prestacion',)
        model=Prestacion
        fields=(
            'codigo_prestacion',
            'codigo_elenco',
            'texto_prestacion',
            'alcance',
            'unidad_medida',
            'posicion',
            'factor_dispersion',
            'grupo_mercologico',
            'precion_prestacion',
            'contrato',
        )

@admin.register(Prestacion)
class PrestacionAdmin(ImportExportModelAdmin):
    resource_class=PrestacionResource
    list_display=(
            'codigo_prestacion',
            'codigo_elenco',
            'texto_prestacion',
            'unidad_medida',
            'posicion',
            'factor_dispersion',
            'grupo_mercologico',
            'precion_prestacion',
            'contrato',
    )
