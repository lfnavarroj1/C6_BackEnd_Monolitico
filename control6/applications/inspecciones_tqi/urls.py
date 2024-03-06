from django.urls import path

from .views import (
    ListarManiobrasTqiView,
    ListarInspectoresView,
    ListarInspectoresParaAsignacionView,
    AsignarInspeccionView,
    EliminarUnaAsignacionView,
    ObtenerMetasTqiView,
    CreateManiobraTqiView,

    ListarContratosPorUnidadesTerritoriales,
    ActualizacionDatosManiobrasTQI,
    ObtenerDetalleManiobraView,
    CalcularCantidadesGenerales,
    ConfirmarInspeccion
)

urlpatterns = [
    path('listar-maniobras-tqi/', ListarManiobrasTqiView.as_view(), name="listar-maniobras-tqi" ),
    path('listar-inspectores/', ListarInspectoresView.as_view(), name="listar-inspectores"),
    path('listar-inspector-asignacion/<pk>', ListarInspectoresParaAsignacionView.as_view(), name="listar-inspector-asignacion"),
    path('obtener-detalle-maniobra/<pk>', ObtenerDetalleManiobraView.as_view(), name="obtener-detalle-maniobra"),
    path('asignar-inspeccion/', AsignarInspeccionView.as_view(), name="asignar-inspeccion"),
    path('eliminar-asignacion/<pk>', EliminarUnaAsignacionView.as_view(), name="eliminar-asignacion"),
    path('obtener-metas-tqi/', ObtenerMetasTqiView.as_view(), name="obtener-metas-tqi"),
    path('crear-maniobra/', CreateManiobraTqiView.as_view(), name="crear-maniobra"),

    # path('listar-contratos/', ListarContratosPorUnidadesTerritoriales.as_view(), name="'lista-contratos"),
    # path('actualizar-data/', ActualizacionDatosManiobrasTQI.as_view(), name="actualizar-data"),
    # path('calcular/', CalcularCantidadesGenerales.as_view(), name="calculos-tqi"),
    # path('confirmar-inspeccion/', ConfirmarInspeccion.as_view(), name="confirmar-inspeccion"),
]

