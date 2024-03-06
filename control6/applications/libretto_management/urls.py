from django.urls import path
from .views import(
    CrearLibretoView,
    ListarLibretosTrabajoView,
    ObtenerDetalleLibretoView,
    ActualizarLibretoView,
    EliminarLibretoView,
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('crear-libreto/', CrearLibretoView.as_view(), name="crear-libreto" ),
    path('listar-libretos-trabajo/<pk>', ListarLibretosTrabajoView.as_view(), name="listar-libretos-trabajo" ),
    path('obtener-detalle-libreto/<pk>', ObtenerDetalleLibretoView.as_view(), name="obtener-detalle-libreto" ),
    path('actualizar-libreto/<pk>', ActualizarLibretoView.as_view(), name="actualizar-libreto" ),
    path('eliminar-libreto/<pk>', EliminarLibretoView.as_view(), name="eliminar-libreto" ),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

