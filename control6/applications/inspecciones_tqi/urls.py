from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    ListarPdlTqi,
    ListarContratosPorUnidadesTerritoriales,
    ListarInspectoresPorUnidadesTerritoriales,
    ActualizacionDatosManiobrasTQI,
    ObtenerManiobra,
    AsignarInspeccion,
    EliminarUnaAsignacion,
    CreateManiobraTqi
)



urlpatterns = [
    # Trabajos
    path('lista/', ListarPdlTqi.as_view(), name="'pdl-list" ),
    path('lista-contratos/', ListarContratosPorUnidadesTerritoriales.as_view(), name="'lista-contratos"),
    path('lista-inspector/', ListarInspectoresPorUnidadesTerritoriales.as_view(), name="'lista-inspector"),
    path('actualizar-data/', ActualizacionDatosManiobrasTQI.as_view(), name="actualizar-data"),
    path('detalle-maniobra/<pk>', ObtenerManiobra.as_view(), name="detalle-maniobra"),
    path('asignacion/', AsignarInspeccion.as_view(), name="asignacion"),
    path('eliminar/<pk>', EliminarUnaAsignacion.as_view(), name="eliminar"),
    path('crear-maniobra/', CreateManiobraTqi.as_view(), name="crear-maniobra"),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

