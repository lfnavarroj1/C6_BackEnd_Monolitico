from django.urls import path
from .views import(
    CrearOdm,
    ListarOdm,
    ObtenerOdm,
    ActualizarOdm,
    EliminarOdm,
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Odm
    path('cargar-odm/', CrearOdm.as_view(), name="cargar-odm" ),
    path('listar-odm/<pk>', ListarOdm.as_view(), name="listar-odm" ),
    path('detalle-odm/<pk>', ObtenerOdm.as_view(), name="'detalle-odm" ),
    path('actualizar-odm/<pk>', ActualizarOdm.as_view(), name="'actualizar-odm" ),
    path('eliminar-odm/<pk>', EliminarOdm.as_view(), name="eliminar-odm" ),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

