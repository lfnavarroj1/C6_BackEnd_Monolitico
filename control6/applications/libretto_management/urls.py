from django.urls import path
from .views import(
    CargarLibreto,
    ListarLibreto,
    ObtenerLibreto,
    ActualizarLibreto,
    EliminarLibreto,
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('cargar-libreto/', CargarLibreto.as_view(), name="cargar-libreto" ),# Revisar el proceso para eliminar.
    path('listar-libreto/<pk>', ListarLibreto.as_view(), name="listar-libreto" ),
    path('detallar-libreto/<pk>', ObtenerLibreto.as_view(), name="'detalle-libreto" ),
    path('actualizar-libreto/<pk>', ActualizarLibreto.as_view(), name="'actualizar-libreto" ),
    path('eliminar-libreto/<pk>', EliminarLibreto.as_view(), name="eliminar-libreto" ),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

