from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Customer


class CustomerResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('customer_number',)
        model = Customer
        fields = (
            'customer_number',
            'transformer',
            'address',
        )

@admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin):
    resource_class = CustomerResource
    list_display = (
        'customer_number',
        'transformer',
        'address',
)

    search_fields = (
        'customer_number',
    )