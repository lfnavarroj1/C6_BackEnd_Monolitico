from django.urls import path
from .views import(
    AgregarLclView,
    ListarLclView,
    ListarLclTrabajoView,
    ObtenerDetalleLclView,
    ActualizarLclView,
    EliminarLclView,
    ContarLclPorProcesosView,
    ContarLclPorEstadoView,
)

urlpatterns = [
    path('agregar-lcl/', AgregarLclView.as_view(), name="agregar-lcl" ),
    path('listar-lcl-todas/', ListarLclView.as_view(), name="listar-lcl-todas" ),
    path('listar-lcl-trabajo/<pk>', ListarLclTrabajoView.as_view(), name="listar-lcl-trabajo" ),
    path('obtener-detalle-lcl/<pk>', ObtenerDetalleLclView.as_view(), name="'obtener-detalle-lcl" ),
    path('actualizar-lcl/<pk>', ActualizarLclView.as_view(), name="'actualizar-lcl" ),
    path('eliminar-lcl/<pk>', EliminarLclView.as_view(), name="eliminar-lcl" ),
    path('contar-lcl-proceso/', ContarLclPorProcesosView.as_view(), name="contartodo-lcl" ),
    path('contar-lcl-estado/', ContarLclPorEstadoView.as_view(), name="contarestado-lcl" ),
]

