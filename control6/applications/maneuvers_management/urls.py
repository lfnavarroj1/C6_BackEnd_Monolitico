from django.urls import path


from django.conf import settings
from django.conf.urls.static import static
from .views import *


urlpatterns = [

    # # Maniobras
    path('cargar-maniobra/', CrearManiobra.as_view(), name="cargar-maniobra" ),
    path('listar-maniobra/<pk>', ListarManiobras.as_view(), name="listar-maniobra" ),
    path('detalle-maniobra/<pk>', ObtenerManiobra.as_view(), name="'detalle-maniobra" ),
    path('actualizar-maniobra/<pk>', ActualizarManiobra.as_view(), name="'actualizar-maniobra" ),
    path('eliminar-maniobra/<pk>', EliminarManiobra.as_view(), name="eliminar-maniobra" ),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

