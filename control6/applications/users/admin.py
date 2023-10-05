from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import User, C6Modules

# Register your models here.

# admin.site.register(User)
admin.site.register(C6Modules)

# Users
class UserResource(resources.ModelResource):
    class Meta:
        model=User
        fields=(
            'username',
            'assigned',
            'phone_number',
        )

@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_class=UserResource
    list_display=(
            'username',
            'assigned',
            'phone_number',
    )