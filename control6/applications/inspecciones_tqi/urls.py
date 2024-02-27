from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    ListarPdlTqi,
    ListarContratosPorUnidadesTerritoriales,
    ListarInspectores,
    ActualizacionDatosManiobrasTQI,
    ObtenerManiobra,
    AsignarInspeccion,
    EliminarUnaAsignacion,
    CreateManiobraTqi,
    CalcularCantidadesGenerales,
    ListarInspectoresParaAsignacion,
    ObtenerMetasTqi,
    ConfirmarInspeccion
)

urlpatterns = [
    # Trabajos
    path('lista/', ListarPdlTqi.as_view(), name="'pdl-list" ),
    path('lista-contratos/', ListarContratosPorUnidadesTerritoriales.as_view(), name="'lista-contratos"),
    path('lista-inspector/', ListarInspectores.as_view(), name="'lista-inspector"),
    path('lista-inspector-asignacion/<pk>', ListarInspectoresParaAsignacion.as_view(), name="'lista-inspector-asinacion"),
    path('actualizar-data/', ActualizacionDatosManiobrasTQI.as_view(), name="actualizar-data"),
    path('detalle-maniobra/<pk>', ObtenerManiobra.as_view(), name="detalle-maniobra"),
    path('asignacion/', AsignarInspeccion.as_view(), name="asignacion"),
    path('eliminar/<pk>', EliminarUnaAsignacion.as_view(), name="eliminar"),
    path('crear-maniobra/', CreateManiobraTqi.as_view(), name="crear-maniobra"),
    path('calcular/', CalcularCantidadesGenerales.as_view(), name="calculos-tqi"),
    path('obtener-metas-tqi/', ObtenerMetasTqi.as_view(), name="obtener-metas-tqi"),
    path('confirmar-inspeccion/', ConfirmarInspeccion.as_view(), name="confirmar-inspeccion"),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

