from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import HoraExtra,CalendarioFestivo


# CALENDARIO FESTIVOS
class CalendarioFestivoResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('id_festivo',)
        model=CalendarioFestivo
        fields=(
            'id_festivo',
            'fecha',
            'celebracion',
        )

@admin.register(CalendarioFestivo)
class CalendarioFestivoAdmin(ImportExportModelAdmin):
    resource_class=CalendarioFestivoResource
    list_display=(
        'id_festivo',
        'fecha',
        'celebracion',
    )
    search_fields=(
        'fecha',
    )


# HORAS EXTRAS
class HorasExtrasResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('id_hora_extra',)
        model=HoraExtra
        fields=(
            'id_hora_extra',
            'usuario',
            'fecha',
            'hora_entrada',
            'hora_salida',
            'observacion',
            'estado',
        )

@admin.register(HoraExtra)
class TrabajoAdmin(ImportExportModelAdmin):
    resource_class=HorasExtrasResource
    list_display=(
        'id_hora_extra',
        'usuario',
        'fecha',
        'hora_entrada',
        'hora_salida',
        'observacion',
        'estado',
    )
    search_fields=(
        'fecha',
    )
    list_filter=(
        'usuario',
    )
