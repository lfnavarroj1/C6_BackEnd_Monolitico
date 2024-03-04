from django.urls import path

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
    path('listar/', ListarPdlTqi.as_view(), name="'pdl-list" ),
    path('listar-contratos/', ListarContratosPorUnidadesTerritoriales.as_view(), name="'lista-contratos"),
    path('listar-inspector/', ListarInspectores.as_view(), name="'lista-inspector"),
    path('listar-inspector-asignacion/<pk>', ListarInspectoresParaAsignacion.as_view(), name="'lista-inspector-asinacion"),
    # path('actualizar-data/', ActualizacionDatosManiobrasTQI.as_view(), name="actualizar-data"),
    path('detallar-maniobra/<pk>', ObtenerManiobra.as_view(), name="detalle-maniobra"),
    path('asignar/', AsignarInspeccion.as_view(), name="asignacion"),
    path('eliminar-asignacion/<pk>', EliminarUnaAsignacion.as_view(), name="eliminar"),
    path('crear-maniobra/', CreateManiobraTqi.as_view(), name="crear-maniobra"),
    # path('calcular/', CalcularCantidadesGenerales.as_view(), name="calculos-tqi"),
    path('obtener-metas-tqi/', ObtenerMetasTqi.as_view(), name="obtener-metas-tqi"),
    # path('confirmar-inspeccion/', ConfirmarInspeccion.as_view(), name="confirmar-inspeccion"),
]

