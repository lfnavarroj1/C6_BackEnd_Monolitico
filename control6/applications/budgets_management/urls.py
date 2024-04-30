# from django.urls import path
# from .views import(
#     AgregarValorizacionView,
#     ListarValorizacionTodoView,
#     ListarValorizacionTrabajoView,
#     ObtenerDetalleValorizacionView,
#     ActualizarValorizacionView,
#     EliminarValorizacionView,
#     CalcularValorizacionView,
#     ListarNodosTrabajoView,
#     ObtenerDetalleNodoView,
#     ListarNodosLclView,
#     ListarPrestaionesValorizacionView,
#     ListarMaterialesValorizacionView,
# )
# from django.conf import settings
# from django.conf.urls.static import static


# urlpatterns = [ 
#     path('agregar-presupuesto/', AgregarValorizacionView.as_view(), name="agregar-presupuesto"),
#     path('listar-presupuesto-todos/', ListarValorizacionTodoView.as_view(), name="listar-presupuesto-todos"),
#     path('listar-presupuesto-trabajo/<pk>', ListarValorizacionTrabajoView.as_view(), name="listar-presupuesto-trabajo"),
#     path('detallar-presupuesto/<pk>', ObtenerDetalleValorizacionView.as_view(), name="'detallar-presupuesto"),
#     path('actualizar-presupuesto/<pk>', ActualizarValorizacionView.as_view(), name="'actualizar-presupuesto"),
#     path('eliminar-presupuesto/<pk>', EliminarValorizacionView.as_view(), name="eliminar-presupuesto"),
#     path('calcular-presupuesto/<pk>', CalcularValorizacionView.as_view(), name="calcular-presupuesto"),
#     path('listar-nodos-trabajo/<pk>', ListarNodosTrabajoView.as_view(), name="listar-nodos-trabajo"),
#     path('ObtenerDetalleNodo/<pk>', ObtenerDetalleNodoView.as_view(), name="ObtenerDetalleNodo"),
#     path('listar-nodos-lcl/<pk>', ListarNodosLclView.as_view(), name="listar-nodos-lcl"),
#     path('listar-prestaciones-presupuesto/<pk>', ListarPrestaionesValorizacionView.as_view(), name="listar-prestaciones-presupuesto"),
#     path('listar-materiales-presupuesto/<pk>', ListarMaterialesValorizacionView.as_view(), name="listar-materiales-presupuesto"),
# ] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)