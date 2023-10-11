from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models.nivel_tension import NivelTension
from .models.subestacion import Subestacion
from .models.circuito import Circuito
from .models.unidad_territorial import UnidadTerritorial
from .models.municipio import Municipio
from .models.vereda import Vereda
from .models.proceso import Proceso
from .models.estado_trabajo import EstadoTrabajo
from .models.estructura_presupuestal import EstructuraPresupuestal
from .models.tipo_instalacion import TipoInstalacion
from .models.cuadrilla import Cuadrilla
from .models.contrato import Contrato
from .models.ruta_proceso import RutaProceso, ModuloBandeja


# Register your models here.

# NIVEL TENSIÓN
class NivelTensionResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('nivel',)
        model=NivelTension
        fields=(
            'nivel',
            'rango',
            'valor_nominal_v',
        )

@admin.register(NivelTension)
class NivelTensionAdmin(ImportExportModelAdmin):
    resource_class=NivelTensionResource
    list_display=(
        'nivel',
        'rango',
        'valor_nominal_v',
    )


# SUBESTACIÓN
class SubestacionResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('codigo',)
        model=Subestacion
        fields=(
            'codigo',
            'nombre',
            'nivel_tension'
        )

@admin.register(Subestacion)
class SubestacionAdmin(ImportExportModelAdmin):
    resource_class=SubestacionResource
    list_display=(
        'codigo',
        'nombre',
        'nivel_tension'
    )


# CIRCUITOS
class CircuitoResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('codigo_circuito',)
        model=Circuito
        fields=(
            'codigo_circuito',
            'ubicacion_tecnica',
            'nombre',
            'subestacion',
            'tesniones_nominales',
            'longitud_aerea_mt',
            'logitud_subterranea_mt',
            'cantidad_clientes'
        )

@admin.register(Circuito)
class CircuitoAdmin(ImportExportModelAdmin):
    resource_class=CircuitoResource
    list_display=(
        'codigo_circuito',
        'ubicacion_tecnica',
        'nombre',
        'subestacion',
        # 'tesniones_nominales',
        'longitud_aerea_mt',
        'logitud_subterranea_mt',
        'cantidad_clientes'
    )


# UNIDAD TERRITORIAL
class UnidadTerritorialResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('numero',)
        model=UnidadTerritorial
        fields=(
            'numero',
            'nombre',
            'jefe',
        )

@admin.register(UnidadTerritorial)
class UnidadTerritorialAdmin(ImportExportModelAdmin):
    resource_class=UnidadTerritorialResource
    list_display=(
        'numero',
        'nombre',
        'jefe',
    )


# MUNICIPIO
class MunicipioResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('codigo_municipio',)
        model=Municipio
        fields=(
            'codigo_municipio',
            'nombre',
            'unidad_territorial',
        )

@admin.register(Municipio)
class MunicipioAdmin(ImportExportModelAdmin):
    resource_class=MunicipioResource
    list_display=(
        'codigo_municipio',
        'nombre',
        'unidad_territorial',
    )


# VEREDA
class VeredaResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('codigo_vereda',)
        model=Vereda
        fields=(
            'codigo_vereda',
            'nombre_vereda',
            'municipio',
            'factor_dispersion',

    )

@admin.register(Vereda)
class VeredaAdmin(ImportExportModelAdmin):
    resource_class=VeredaResource
    list_display=(
        'codigo_vereda',
        'nombre_vereda',
        'municipio',
        'factor_dispersion',
    )


# PROCESO
class ProcesoResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('codigo_proceso',)
        model=Proceso
        fields=(
            'codigo_proceso',
            'nombre',
            'descripcion',
        )

@admin.register(Proceso)
class ProcessAdmin(ImportExportModelAdmin):
    resource_class=ProcesoResource
    list_display=(
        'codigo_proceso',
        'nombre',
        'descripcion',
    )


# ESTADO
class EstadoTrabajoResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('id_estado',)
        model=EstadoTrabajo
        fields=(
            'id_estado',
            'nombre',
            'descripcion',
        )

@admin.register(EstadoTrabajo)
class EstadoTrabajoAdmin(ImportExportModelAdmin):
    resource_class=EstadoTrabajoResource
    list_display=(
            'id_estado',
            'nombre',
            'descripcion',
    )


# ESTRUCTURA PRESUPUESTAL
class EstructuraPresupuestalResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('id_estructura_pptal',)
        model=EstructuraPresupuestal
        fields=(
            'id_estructura_pptal',
            'nombre_corto',
            'anio',
            'macrocategoria',
            'ir',
            'proyecto',
            'indicador_impuesto',
        )

@admin.register(EstructuraPresupuestal)
class EstructuraPresupuestalAdmin(ImportExportModelAdmin):
    resource_class=EstructuraPresupuestalResource
    list_display=(
            'id_estructura_pptal',
            'nombre_corto',
            'anio',
            'macrocategoria',
            'ir',
            'proyecto',
            'indicador_impuesto',
    )


# TIPO INSTALACION
class TipoInstalacionResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('id_tipo',)
        model=TipoInstalacion
        fields=(
            'id_tipo',
            'nombre',
        )

@admin.register(TipoInstalacion)
class TipoInstalacionAdmin(ImportExportModelAdmin):
    resource_class=TipoInstalacionResource
    list_display=(
            'id_tipo',
            'nombre',
    )


# CUADRILLA
class CuadrillaResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('codigo_cuadrilla',)
        model=Cuadrilla
        fields=(
            'codigo_cuadrilla',
            'nombre',
            'tipo_cuadrilla',
        )

@admin.register(Cuadrilla)
class CuadrillaAdmin(ImportExportModelAdmin):
    resource_class=CuadrillaResource
    list_display=(
            'codigo_cuadrilla',
            'nombre',
            'tipo_cuadrilla',
    )


# CONTRATO
class ContratoResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('numero_contrato',)
        model=Contrato
        fields=(
            'numero_contrato',
            'nombre',
            'objeto',
        )

@admin.register(Contrato)
class ContratoAdmin(ImportExportModelAdmin):
    resource_class=ContratoResource
    list_display=(
            'numero_contrato',
            'nombre',
            'objeto',
    )


# RUTA PROCESO
class RutaProcesoResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('codigo_ruta',)
        model=RutaProceso
        fields=(
            'codigo_ruta',
            'proceso',
            'modulos',
            'paso',
            'estado',
        )

@admin.register(RutaProceso)
class RutaProcesoAdmin(ImportExportModelAdmin):
    resource_class=RutaProcesoResource
    list_display=(
        'codigo_ruta',
        'proceso',
        'paso',
        'estado',
    )

# MODULOS
class ModuloBandejaResource(resources.ModelResource):
    class Meta:
        import_id_fields = ('id_modulo',)
        model=ModuloBandeja
        fields=(
            'id_modulo',
            'nombre',
        )

@admin.register(ModuloBandeja)
class ModuloBandejaAdmin(ImportExportModelAdmin):
    resource_class=ModuloBandejaResource
    list_display=(
            'id_modulo',
            'nombre',
    )


