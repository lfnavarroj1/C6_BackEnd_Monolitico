from django.urls import path
from .views.trabajo_view import (
ListarTrabajos, 
CrearTrabajo, 
ActualizarTrabajo, 
ActualizarParcialTrabajo,
EliminarTrabajo,
ObtenerTrabajo,
)

urlpatterns = [
    path('lista/', ListarTrabajos.as_view(), name="'work-list" ),
    path('crear/', CrearTrabajo.as_view(), name="'work-create" ),
    path('actualizar/<pk>', ActualizarTrabajo.as_view(), name="'work-update" ),
    path('actualizarparcial/<pk>', ActualizarParcialTrabajo.as_view(), name="'work-partial-update" ),
    path('eliminar/<pk>', EliminarTrabajo.as_view(), name="'work-delete" ),
    path('detalle/<pk>', ObtenerTrabajo.as_view(), name="'work-detail" ),
]

