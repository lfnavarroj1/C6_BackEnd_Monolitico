from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Contrat, TechnicalTeam


class ContratResource(resources.ModelResource):
    class Meta:
        model = Contrat
        import_id_fields = ('code',)
        fields = (
            'code',
            'name',
            'objetive',
            'territorial_units',
            'management_unit',
            'active',
        )

@admin.register(Contrat)
class ContratAdmin(ImportExportModelAdmin):
    resource_class = Contrat
    list_display = (
        'code',
        'name',
        'objetive',
        'management_unit',
        'active',
    )


class TechnicalTeamResource(resources.ModelResource):
    class Meta:
        model = TechnicalTeam
        import_id_fields = ('code',)
        fields = (
            'code',
            'name',
            'type',
            'process_group',
            'contrat',
        )

@admin.register(TechnicalTeam)
class TechnicalTeamAdmin(ImportExportModelAdmin):
    resource_class = TechnicalTeamResource
    list_display = (
        'code',
        'name',
        'type',
        'process_group',
        'contrat',
    )
