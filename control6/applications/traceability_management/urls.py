from django.urls import path
from .views import(
    CrearTrazabilidadTrabajo,
    ListarTrazabilidadTrabajo,
    CrearTrazabilidadInspeccionesTqi,
    ListarTrazabilidadInspeccionesTqi,
)

urlpatterns = [
    path('crear_trazabilidad_trabajo/', CrearTrazabilidadTrabajo.as_view(), name="crear-traza" ),
    path('listar_trazabilidad_trabajo/<pk>', ListarTrazabilidadTrabajo.as_view(), name="listar-trazabilidad" ),
    path('crear_trazabilidad_inspeccion_tqi/', CrearTrazabilidadInspeccionesTqi.as_view(), name="crear-traza" ),
    path('listar_trazabilidad_inspeccion_tqi/<pk>', ListarTrazabilidadInspeccionesTqi.as_view(), name="listar-trazabilidad" ),
]

