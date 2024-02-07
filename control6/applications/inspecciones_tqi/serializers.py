from rest_framework import serializers, pagination
from .models import PdlTqi, Asignaciones, MetasTQI, MetasInspectores, Maniobras
from ..users.models import User

from ..users.serializers import UserSerializer


# proceso (Deuda técnica, optimizar los campos que requiero por vista)

class PdlTqiSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PdlTqi
        fields = (
            'codigo',
            'tipo',
            'descripcion',
            'estado_stweb',
            'fecha_inicio',
            'fecha_fin',
            'hora_inicio',
            'hora_fin',
            'circuito',
            'unidad_territorial',
            'unidad',
            'causal',
            'pdl_asociado',
            'fecha_actualizacion',
            'contrato',
            'municipio',
            'vereda_localidad',
            'direccion',
            'estado_tqi',
            'criticidad_maniobra',
        )


class AsignacionesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Asignaciones
        fields = (
            'id_asignacion',
            'pdl_tqi',
            'cedula_inspector',
            'estado_stweb',
            'cedula_responsable_asignacion',
            'fecha_asignacion',
            'ejecutado',
        )

class MetasTQISerializer(serializers.ModelSerializer):

    class Meta:
        model = MetasTQI
        fields = (
            'unidad_territorial',
            'contrato',
            'anio',
            'mes',
            'cantidad_meta',
            'cantidad_programada',
            'cantidad_ejecutada',
            'fecha_actualizacion',
            'responsable_actualizacion',
        )


class MetasInspectoresSerializer(serializers.ModelSerializer):

    inspector = UserSerializer()

    class Meta:
        model = MetasInspectores
        fields = (
            'inspector',
            'anio',
            'mes',
            'cantidad_meta',
            'cantidad_programada',
            'cantidad_ejecutada',
            'fecha_actualizacion',
            'responsable_actualizacion',
        )

class PdlTqiPagination(pagination.PageNumberPagination):
    page_size = 20
    max_page_size = 100


class ManiobraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maniobras
        fields = (
            'codigo',
            'tipo',
            'fecha_trabajo_inicio',
            'hora_trabajo_inicio',
            'fecha_trabajo_fin',
            'hora_trabajo_fin',
            'fecha_programacion',
            'estado',
            'pdl_asociado',
            'circuito',
            'causal',
            'descripcion',
            'unidad_territorial',
            'unidad_territorial_std',
            'fecha_actualizacion',
            'ubicacion',
            'localidad_municipio',
            'nombre_responsable',
            'unidad_responsable',
            'telefono_reponsable',
            'firma',
            'co'
        )