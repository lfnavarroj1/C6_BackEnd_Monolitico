from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import *


class TerritorialUnitResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('id',)
        model = TerritorialUnit
        fields = (
            'id',
            'name',
        )

@admin.register(TerritorialUnit)
class TerritorialUnitAdmin(ImportExportModelAdmin):
    resource_class = TerritorialUnitResource
    list_display = (
        'id',
        'name',
    )


class MunicipalityResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('code',)
        model = Municipality
        fields = (
            'code',
            'name',
            'territorial_unit',
        )

@admin.register(Municipality)
class MunicipalityAdmin(ImportExportModelAdmin):
    resource_class = MunicipalityResource
    list_display = (
        'code',
        'name',
    )


class SidewalkResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('code',)
        model = Sidewalk
        fields = (
            'code',
            'name',
            'municipality',
            'cft',
            'dispersion_factor',
        )

@admin.register(Sidewalk)
class SidewalkAdmin(ImportExportModelAdmin):
    resource_class = SidewalkResource
    list_display = (
        'code',
        'name',
        'municipality',
        'cft',
        'dispersion_factor',
    )


