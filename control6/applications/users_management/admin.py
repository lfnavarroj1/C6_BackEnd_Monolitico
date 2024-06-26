from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import User, C6Module

class C6ModulesResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('id_module',)
        model = C6Module
        fields = (
            'id_module',
            'name',
            'description',
            'url_module',
        )

@admin.register(C6Module)
class C6ModulesAdmin(ImportExportModelAdmin):
    resource_class=C6ModulesResource
    list_display = (
        'id_module',
        'name',
        'description',
        'url_module',
    )

# Users
class UserResource(resources.ModelResource):
    class Meta:
        model=User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email_address',
            'assigned',
            'phone_number',
            'processes',
            'estado_trabajo',
            'user_modules',
            'unidades_territoriales',
            'contratos',
            'cargo',
            'es_enel',
            'lider_hse',
        )

@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource
    list_display = (
        'username',
        'first_name',
        'last_name',
        'assigned',
    )
    # filter_horizontal = ( 
    #     'procesos',
    #     'estado_trabajo',
    #     'user_modules',
    #     'unidades_territoriales',
    #     'contratos',
    # )
