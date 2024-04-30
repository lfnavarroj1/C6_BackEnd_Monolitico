from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/budgets/', include('applications.budgets_management.urls')),
    # path('api/sistemas_externos/', include('applications.external_systems_management.urls')),
    # path('api/horas_extras/', include('applications.horas_extras.urls')),
    # path('api/inspecciones-tqi/', include('applications.inspecciones_tqi.urls')),
    # path('api/mano_de_obra/', include('applications.labour_management.urls')),
    # path('api/lcl/', include('applications.lcl_management.urls')),
    # path('api/libreto/', include('applications.libretto_management.urls')),
    # path('api/mantenimiento/', include('applications.maintenance_management.urls')),
    # path('api/maniobras/', include('applications.maneuvers_management.urls')),
    # path('api/materiales/', include('applications.materials_management.urls')),
    # path('api/programacion_de_nodos/', include('applications.node_scheduling_management.urls')),
    # path('api/odm/', include('applications.odm_management.urls')),
    # path('api/con_el_tiempo/', include('applications.overtime_management.urls')),
    # path('api/descargos/', include('applications.penalities_management.urls')),
    # path('api/prestaciones/', include('applications.prestaciones.urls')),
    # path('api/programacion/', include('applications.scheduling_management.urls')),
    # path('api/static-data/', include('applications.static_data.urls')),
    # path('api/trazabilidad/', include('applications.traceability_management.urls')),
    # path('api/users/', include('applications.users.urls')),
    # path('api/trabajos/', include('applications.work_management.urls')),
    # path('api/seguimiento_metas/', include('applications.seguimiento_metas.urls')), 
    # path('api/customers_management/', include('applications.customers_management.urls')), 
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
