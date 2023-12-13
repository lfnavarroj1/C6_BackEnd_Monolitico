from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Material

# Register your models here.

# PRESTACIONES
class MaterialResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('codigo_material',)
        model=Material
        fields=(
            'codigo_material',
            'descripcion',
            'unidad_medida',
            'aportacion',
            'precio',
        )

@admin.register(Material)
class MaterialAdmin(ImportExportModelAdmin):
    resource_class=MaterialResource
    list_display=(
            'codigo_material',
            'descripcion',
            'unidad_medida',
            'aportacion',
            'precio',
    )