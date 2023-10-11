from django.urls import path
from .views.trabajo_view import (
ListarTrabajos, 
CrearTrabajo, 
ActualizarTrabajo, 
SiguienteEstado,
AnteriorEstado,
# ActualizarParcialTrabajo,
EliminarTrabajo,
ObtenerTrabajo,

)
from .views.trazabilidad_view import(
    CrearTrazabilidad,
    ListarTrazabilidad
)

urlpatterns = [
    path('lista/', ListarTrabajos.as_view(), name="'work-list" ),
    path('crear/', CrearTrabajo.as_view(), name="'work-create" ),
    path('actualizar/<pk>', ActualizarTrabajo.as_view(), name="'work-update" ),
    # path('actualizarparcial/<pk>', ActualizarParcialTrabajo.as_view(), name="'work-partial-update" ),
    path('eliminar/<pk>', EliminarTrabajo.as_view(), name="'work-delete" ),
    path('detalle/<pk>', ObtenerTrabajo.as_view(), name="'work-detail" ),
    path('siguiente/<pk>', SiguienteEstado.as_view(), name="'siguiente" ),
    path('anterior/<pk>', AnteriorEstado.as_view(), name="'anterior" ),
    # Rutas trazabilidad
    path('crear_traza/', CrearTrazabilidad.as_view(), name="'crear-traza" ),
    path('trazabilidad/<pk>', ListarTrazabilidad.as_view(), name="trazabilidad-trabajo" ),
]

