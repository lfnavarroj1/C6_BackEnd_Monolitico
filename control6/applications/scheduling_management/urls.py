from django.urls import path

from .views import(
    CrearProgramacion,
    ListarProgramacion,
    ObtenerProgramacion,
    ActualizarProgramacion,
    EliminarProgramacion,
    ListarCuadrillasDisponibles,
    ListarCuadrillasTrabajo,
)

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('cargar-programacion/', CrearProgramacion.as_view(), name="cargar-programacion" ),
    path('listar-programacion/<pk>', ListarProgramacion.as_view(), name="listar-programacion" ),
    path('detalle-programacion/<pk>', ObtenerProgramacion.as_view(), name="'detalle-programacion" ),
    path('lista-cuadrillas/<date>', ListarCuadrillasDisponibles.as_view(), name="'lista-cuadrillas" ),
    path('lista-cuadrillasTrabajo/', ListarCuadrillasTrabajo.as_view(), name="'lista-cuadrillasTrabajo" ),
    path('actualizar-programacion/<pk>', ActualizarProgramacion.as_view(), name="'actualizar-programacion" ),
    path('eliminar-programacion/<pk>', EliminarProgramacion.as_view(), name="eliminar-programacion" ),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)