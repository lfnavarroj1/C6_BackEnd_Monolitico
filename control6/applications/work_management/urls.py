from django.urls import path

from .views import (
    ListarTrabajos, 
    CrearTrabajo, 
    ActualizarTrabajo, 
    SiguienteEstado,
    AnteriorEstado,
    EliminarTrabajo,
    ObtenerTrabajo,
    ContarTrabajosPorProcesos,
    ContarTrabajosPorEstado,
    SubirArchivoView,
    EliminarSoporteInicial,
    ListarSoportesIniciales,
)



from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('lista/', ListarTrabajos.as_view(), name="work-list" ),
    path('crear/', CrearTrabajo.as_view(), name="work-create" ),
    path('actualizar/<pk>', ActualizarTrabajo.as_view(), name="work-update" ),
    path('eliminar/<pk>', EliminarTrabajo.as_view(), name="work-delete" ),
    path('detalle/<pk>', ObtenerTrabajo.as_view(), name="work-detail" ),
    path('siguiente/<pk>', SiguienteEstado.as_view(), name="siguiente" ),
    path('anterior/<pk>', AnteriorEstado.as_view(), name="anterior" ),
    path('contar-proceso/', ContarTrabajosPorProcesos.as_view(), name="work-count-process" ),
    path('contar-estado/', ContarTrabajosPorEstado.as_view(), name="work-count-state" ),
    path('cargar-archivo/', SubirArchivoView.as_view(), name="work-count-state" ),
    path('eliminar-archivo/', EliminarSoporteInicial.as_view(), name="work-count-state" ),
    path('listar-archivos/', ListarSoportesIniciales.as_view(), name="work-count-state" ),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

