from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import FrontendModule, Process, StateWork, WorkFlow


class FrontendModuleResource(resources.ModelResource):
    class Meta:
        model = FrontendModule
        import_id_fields = ('id',)
        fields = (
            'id',
            'name',
        )

@admin.register(FrontendModule)
class FrontendModuleAdmin(ImportExportModelAdmin):
    resource_class = FrontendModuleResource
    list_display = (
        'id',
        'name',
    )


class ProcessResource(resources.ModelResource):
    class Meta:
        model = Process
        import_id_fields = ('id',)
        fields = (
            'id',
            'name',
            'description',
        )

@admin.register(Process)
class UserAdmin(ImportExportModelAdmin):
    resource_class =ProcessResource
    list_display = (
        'id',
        'name',
        'description',
    )


class StateWorkResource(resources.ModelResource):
    class Meta:
        model = StateWork
        import_id_fields = ('id',)
        fields = (
            'id',
            'name',
            'description',
        )

@admin.register(StateWork)
class UserAdmin(ImportExportModelAdmin):
    resource_class = StateWorkResource
    list_display = (
        'id',
        'name',
        'description',
    )


class WorkFlowResource(resources.ModelResource):
    class Meta:
        model = WorkFlow
        import_id_fields = ('id',)
        fields = (
            'id',
            'process',
            'modules',
            'step',
            'state_work',
        )

@admin.register(WorkFlow)
class WorkFlowAdmin(ImportExportModelAdmin):
    resource_class = WorkFlowResource
    list_display = (
        'id',
        'process',
        # 'modules',
        'step',
        'state_work',
    )
