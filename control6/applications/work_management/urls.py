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
ContarTrabajosPorProcesos,
ContarTrabajosPorEstado

)
from .views.trazabilidad_view import(
    CrearTrazabilidad,
    ListarTrazabilidad
)

from .views.soportes_iniciales_view import(
    SubirArchivoView,
    EliminarSoporteInicial,
    ListarSoportesIniciales,
    DescargaArchivo
)

from .views.valorizacion_view import(
    CargarValorizacionView,
    ListarValorizacion,
    ObtenerValorizacion,
    ActualizarValorizacion,
    EliminarValorizacion,
    CalcularValorizacion,
    ListarNodosTrabajo,
    ListarNodosLcl
)

from .views.odm_view import(
    CrearOdm,
    ListarOdm,
    ObtenerOdm,
    ActualizarOdm,
    EliminarOdm,
)

from .views.lcl_view import(
    CrearLcl,
    ListarLcl,
    ObtenerLcl,
    ActualizarLcl,
    EliminarLcl,
    ListarTodasLcl,
    ContarLclPorProcesos,
    ContarLclPorEstado,
)

from .views.programacion_view import(
    CrearProgramacion,
    ListarProgramacion,
    ObtenerProgramacion,
    ActualizarProgramacion,
    EliminarProgramacion,
    ListarCuadrillasDisponibles,
    ListarCuadrillasTrabajo,
)

from .views.maniobra_view import(
    CrearManiobra,
    ListarManiobras,
    ObtenerManiobra,
    ActualizarManiobra,
    EliminarManiobra,
)

from .views.libreto_view import(
    CargarLibreto,
    ListarLibreto,
    ObtenerLibreto,
    ActualizarLibreto,
    EliminarLibreto,
)

from .views.nodo_seguimiento_view import(
    ListarNodosSeguimiento,
    ListarNodosProgramados,
    ListarNodosDisponiblesLcl,
    ListarNodosDisponiblesTrabajo,
)

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Trabajos
    path('lista/', ListarTrabajos.as_view(), name="'work-list" ),
    path('crear/', CrearTrabajo.as_view(), name="'work-create" ),
    path('actualizar/<pk>', ActualizarTrabajo.as_view(), name="'work-update" ),
    # path('actualizarparcial/<pk>', ActualizarParcialTrabajo.as_view(), name="'work-partial-update" ),
    path('eliminar/<pk>', EliminarTrabajo.as_view(), name="'work-delete" ),
    path('detalle/<pk>', ObtenerTrabajo.as_view(), name="'work-detail" ),
    path('siguiente/<pk>', SiguienteEstado.as_view(), name="'siguiente" ),
    path('anterior/<pk>', AnteriorEstado.as_view(), name="'anterior" ),
    path('contar/', ContarTrabajosPorProcesos.as_view(), name="'work-count" ),
    path('contar-estado/', ContarTrabajosPorEstado.as_view(), name="'work-count-state" ),

    # Rutas trazabilidad
    path('crear_traza/', CrearTrazabilidad.as_view(), name="'crear-traza" ),
    path('trazabilidad/<pk>', ListarTrazabilidad.as_view(), name="trazabilidad-trabajo" ),
    # Cargue de archivos iniciales
    path('cargar-soportes/', SubirArchivoView.as_view(), name="cargar-soportes" ),
    path('eliminar-soportes/<pk>', EliminarSoporteInicial.as_view(), name="eliminar-soportes" ),
    path('listar-soportes/<pk>', ListarSoportesIniciales.as_view(), name="listar-soportes" ),
    path('descargar-soportes/<id>', DescargaArchivo.as_view(), name="descargar-soportes" ),
    # 2. Presupuesto
    path('cargar-presupuesto/', CargarValorizacionView.as_view(), name="cargar-presupuesto" ),
    path('listar-presupuesto/<pk>', ListarValorizacion.as_view(), name="listar-presupuesto" ),
    path('detalle-presupuesto/<pk>', ObtenerValorizacion.as_view(), name="'detalle-presupuesto" ),
    path('actualizar-presupuesto/<pk>', ActualizarValorizacion.as_view(), name="'actualizar-presupuesto" ),
    path('eliminar-presupuesto/<pk>', EliminarValorizacion.as_view(), name="eliminar-presupuesto" ),
    path('calcular-presupuesto/<pk>', CalcularValorizacion.as_view(), name="calcular-presupuesto" ),
    path('listar-nodos-trabajo/<pk>', ListarNodosTrabajo.as_view(), name="listar-nodos-trabajo" ),
    path('listar-nodos-lcl/', ListarNodosLcl.as_view(), name="listar-nodos-lcl" ),
    # Odm
    path('cargar-odm/', CrearOdm.as_view(), name="cargar-odm" ),
    path('listar-odm/<pk>', ListarOdm.as_view(), name="listar-odm" ),
    path('detalle-odm/<pk>', ObtenerOdm.as_view(), name="'detalle-odm" ),
    path('actualizar-odm/<pk>', ActualizarOdm.as_view(), name="'actualizar-odm" ),
    path('eliminar-odm/<pk>', EliminarOdm.as_view(), name="eliminar-odm" ),
    # Lcl
    path('cargar-lcl/', CrearLcl.as_view(), name="cargar-lcl" ),
    path('listar-lcl/<pk>', ListarLcl.as_view(), name="listar-lcl" ),
    path('detalle-lcl/<pk>', ObtenerLcl.as_view(), name="'detalle-lcl" ),
    path('actualizar-lcl/<pk>', ActualizarLcl.as_view(), name="'actualizar-lcl" ),
    path('eliminar-lcl/<pk>', EliminarLcl.as_view(), name="eliminar-lcl" ),
    path('listartodolcl/', ListarTodasLcl.as_view(), name="listartodo-lcl" ),
    path('contartodolcl/', ContarLclPorProcesos.as_view(), name="contartodo-lcl" ),
    path('contarestadolcl/', ContarLclPorEstado.as_view(), name="contarestado-lcl" ),
    # # Programación
    path('cargar-programacion/', CrearProgramacion.as_view(), name="cargar-programacion" ),
    path('listar-programacion/<pk>', ListarProgramacion.as_view(), name="listar-programacion" ),
    path('detalle-programacion/<pk>', ObtenerProgramacion.as_view(), name="'detalle-programacion" ),
    path('lista-cuadrillas/<date>', ListarCuadrillasDisponibles.as_view(), name="'lista-cuadrillas" ),
    path('lista-cuadrillasTrabajo/', ListarCuadrillasTrabajo.as_view(), name="'lista-cuadrillasTrabajo" ),
    path('actualizar-programacion/<pk>', ActualizarProgramacion.as_view(), name="'actualizar-programacion" ),
    path('eliminar-programacion/<pk>', EliminarProgramacion.as_view(), name="eliminar-programacion" ),
    # # Maniobras
    path('cargar-maniobra/', CrearManiobra.as_view(), name="cargar-maniobra" ),
    path('listar-maniobra/<pk>', ListarManiobras.as_view(), name="listar-maniobra" ),
    path('detalle-maniobra/<pk>', ObtenerManiobra.as_view(), name="'detalle-maniobra" ),
    path('actualizar-maniobra/<pk>', ActualizarManiobra.as_view(), name="'actualizar-maniobra" ),
    path('eliminar-maniobra/<pk>', EliminarManiobra.as_view(), name="eliminar-maniobra" ),
    # # Libretos
    path('cargar-libreto/', CargarLibreto.as_view(), name="cargar-libreto" ),# Revisar el proceso para eliminar.
    path('listar-libreto/<pk>', ListarLibreto.as_view(), name="listar-libreto" ),
    path('detalle-libreto/<pk>', ObtenerLibreto.as_view(), name="'detalle-libreto" ),
    path('actualizar-libreto/<pk>', ActualizarLibreto.as_view(), name="'actualizar-libreto" ),
    path('eliminar-libreto/<pk>', EliminarLibreto.as_view(), name="eliminar-libreto" ),

    # # Nodos Seguimiento
    path('listar-nodos-seguimiento/<pk>', ListarNodosSeguimiento.as_view(), name="listar-nodos-programacion" ),
    path('listar-nodos-programados/<pk>', ListarNodosProgramados.as_view(), name="listar-nodos-programados" ),
    path('listar-nodos-disponibles-lcl/', ListarNodosDisponiblesLcl.as_view(), name="listar-nodos-disponibles-lcl" ),
    path('listar-nodos-disponibles-trabajo/<pk>', ListarNodosDisponiblesTrabajo.as_view(), name="listar-nodos-disponibles-trabajo" ),
    


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

