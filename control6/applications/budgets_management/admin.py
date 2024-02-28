from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Valorizacion


class ValorizacionResource(resources.ModelResource):
    class Meta:
        model=Valorizacion
        fields=(
            'id_valorizacion',
            'trabajo',
            'monto_mano_obra',
            'monto_materiales',
            'estado',
            'nivel_tension',
            'presupuesto',
        )

@admin.register(Valorizacion)
class ValorizacionAdmin(ImportExportModelAdmin):
    resource_class=ValorizacionResource
    list_display=(
        'id_valorizacion',
        'trabajo',
        'monto_mano_obra',
        'monto_materiales',
        'estado',
        'nivel_tension',
        'presupuesto',
    )

