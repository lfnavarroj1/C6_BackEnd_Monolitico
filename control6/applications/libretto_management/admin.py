from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Libreto

# LIBRETOS
class LibretoResource(resources.ModelResource):
    class Meta:
        model=Libreto
        fields=(
            "id_libreto",
            "programacion",
            "numero_libreto",
            "valor_mod",
            "valor_mat",
            "observacion",
            "planillas_conciliacion",
            "planillas_firmadas",
            "estado_libreto",
            "es_ultimo_libreto",
            "trabajo",
        )

@admin.register(Libreto)
class LibretoAdmin(ImportExportModelAdmin):
    resource_class=LibretoResource
    list_display=(
            "id_libreto",
            "programacion",
            "numero_libreto",
            "valor_mod",
            "valor_mat",
            "observacion",
            "planillas_conciliacion",
            "planillas_firmadas",
            "estado_libreto",
            "es_ultimo_libreto",
            "trabajo",
    )
