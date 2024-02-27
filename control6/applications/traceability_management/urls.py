from django.urls import path


from .views.trazabilidad_view import(
    CrearTrazabilidad,
    ListarTrazabilidad
)





from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Rutas trazabilidad
    path('crear_traza/', CrearTrazabilidad.as_view(), name="'crear-traza" ),
    path('trazabilidad/<pk>', ListarTrazabilidad.as_view(), name="trazabilidad-trabajo" ),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

