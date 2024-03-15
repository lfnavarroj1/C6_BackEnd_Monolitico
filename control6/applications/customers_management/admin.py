from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Customer
from django.utils.encoding import smart_str
from django.http import StreamingHttpResponse


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



    def exportar_csv(self, request, queryset):
        def generar_csv():
            yield ','.join([field.name for field in Customer._meta.fields]) + '\n'
            for obj in queryset.iterator(chunk_size=1000):  # Paginación para evitar cargar todos los registros en memoria
                yield ','.join([smart_str(getattr(obj, field.name, '')) for field in Customer._meta.fields]) + '\n'

        response = StreamingHttpResponse(generar_csv(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        return response