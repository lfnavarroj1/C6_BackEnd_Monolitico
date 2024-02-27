from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Lcl

# LCL
class LclResource(resources.ModelResource):
    class Meta:
        model=Lcl
        fields=(
            'lcl',
            'estado_lcl',
            'indicador_impuesto',
            'valor_mano_obra',
            'valor_materiales',
            'responsable_scm',
            'texto_scm',
            'alcance',
            'odms',
        )

@admin.register(Lcl)
class LclAdmin(ImportExportModelAdmin):
    resource_class=LclResource
    list_display=(
        'lcl',
        'estado_lcl',
        'indicador_impuesto',
        'valor_mano_obra',
        'valor_materiales',
        'responsable_scm',
        'texto_scm',
        'alcance',
        #'odms',
    )


