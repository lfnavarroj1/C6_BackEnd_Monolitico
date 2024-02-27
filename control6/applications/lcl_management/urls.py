from django.urls import path
from .views import(
    CrearLcl,
    ListarLcl,
    ObtenerLcl,
    ActualizarLcl,
    EliminarLcl,
    ListarTodasLcl,
    ContarLclPorProcesos,
    ContarLclPorEstado,
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Lcl
    path('cargar-lcl/', CrearLcl.as_view(), name="cargar-lcl" ),
    path('listar-lcl/<pk>', ListarLcl.as_view(), name="listar-lcl" ),
    path('detalle-lcl/<pk>', ObtenerLcl.as_view(), name="'detalle-lcl" ),
    path('actualizar-lcl/<pk>', ActualizarLcl.as_view(), name="'actualizar-lcl" ),
    path('eliminar-lcl/<pk>', EliminarLcl.as_view(), name="eliminar-lcl" ),
    path('listartodolcl/', ListarTodasLcl.as_view(), name="listartodo-lcl" ),
    path('contartodolcl/', ContarLclPorProcesos.as_view(), name="contartodo-lcl" ),
    path('contarestadolcl/', ContarLclPorEstado.as_view(), name="contarestado-lcl" ),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

