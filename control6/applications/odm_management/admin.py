from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Odm 

# ODM
class OdmResource(resources.ModelResource):
    class Meta:
        model=Odm
        fields=(
            'odm',
            'valorizacion',
            'agp',
            'protocolo',
            'solicitud',
        )

@admin.register(Odm)
class OdmAdmin(ImportExportModelAdmin):
    resource_class=OdmResource
    list_display=(
        'odm',
        'valorizacion',
        'agp',
        'protocolo',
        'solicitud',
    )