from django.urls import path
from .views import(
    CargarValorizacionView,
    ListarValorizacion,
    ObtenerValorizacion,
    ActualizarValorizacion,
    EliminarValorizacion,
    CalcularValorizacion,
    ListarNodosTrabajo,
    ListarNodosLcl
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # 2. Presupuesto
    path('cargar-presupuesto/', CargarValorizacionView.as_view(), name="cargar-presupuesto" ),
    path('listar-presupuesto/<pk>', ListarValorizacion.as_view(), name="listar-presupuesto" ),
    path('detalle-presupuesto/<pk>', ObtenerValorizacion.as_view(), name="'detalle-presupuesto" ),
    path('actualizar-presupuesto/<pk>', ActualizarValorizacion.as_view(), name="'actualizar-presupuesto" ),
    path('eliminar-presupuesto/<pk>', EliminarValorizacion.as_view(), name="eliminar-presupuesto" ),
    path('calcular-presupuesto/<pk>', CalcularValorizacion.as_view(), name="calcular-presupuesto" ),
    path('listar-nodos-trabajo/<pk>', ListarNodosTrabajo.as_view(), name="listar-nodos-trabajo" ),
    path('listar-nodos-lcl/', ListarNodosLcl.as_view(), name="listar-nodos-lcl" ),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)