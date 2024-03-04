from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    CrearTrabajoView,
    ListarTrabajosView,
    ObtenerDetalleTrabajoView,
    ActualizarTrabajoView,
    EliminarTrabajoView,
    SiguienteEstadoView,
    AnteriorEstadoView,
    ContarTrabajosPorProcesosView,
    ContarTrabajosPorEstadoView,
    SubirArchivoView,
    EliminarSoporteInicialView,
    ListarSoportesInicialesView
)

urlpatterns = [
    path('crear/', CrearTrabajoView.as_view(), name="work-create" ),
    path('lista/', ListarTrabajosView.as_view(), name="work-list" ),
    path('detalle/<pk>', ObtenerDetalleTrabajoView.as_view(), name="work-detail" ),
    path('actualizar/<pk>', ActualizarTrabajoView.as_view(), name="work-update" ),
    path('eliminar/<pk>', EliminarTrabajoView.as_view(), name="work-delete" ),
    path('siguiente/<pk>', SiguienteEstadoView.as_view(), name="siguiente" ),
    path('anterior/<pk>', AnteriorEstadoView.as_view(), name="anterior" ),
    path('contar-proceso/', ContarTrabajosPorProcesosView.as_view(), name="work-count-process" ),
    path('contar-estado/', ContarTrabajosPorEstadoView.as_view(), name="work-count-state" ),
    path('cargar-archivo/', SubirArchivoView.as_view(), name="work-count-state" ),
    path('eliminar-archivo/<pk>', EliminarSoporteInicialView.as_view(), name="work-count-state" ),
    path('listar-archivos/<pk>', ListarSoportesInicialesView.as_view(), name="work-count-state" ),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

