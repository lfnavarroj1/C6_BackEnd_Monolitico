from rest_framework import serializers, pagination
from .models import ManiobrasTqi, MetasTQI, MetasInspectores
from ..users.models import User
from ..users.serializers import UserSerializer
from ..static_data.serializers.contrato_serializer import ContratoSerializer


class ManiobrasTqiSerializer(serializers.ModelSerializer):

    inspector_asingado = UserSerializer(allow_null=True, required=False)
    
    class Meta:
        model = ManiobrasTqi
        fields = (
            'codigo',
            'tipo',
            'descripcion',
            'estado_stweb',
            'fecha_inicio',
            'fecha_fin',
            'hora_inicio',
            'hora_fin',
            'pdl_asociado',
            'fecha_actualizacion',
            'unidad_territorial',
            'subestacion',
            'circuito',
            'unidad_ejecutora',
            'causal',
            'contrato',
            'municipio',
            'vereda_localidad',
            'direccion',
            'estado_tqi',
            'criticidad_maniobra',
            'cuadrilla_responsable',
            'telefono_cuadrilla_responsable',
            'inspector_asingado',
            'inspeccion_ejecutada',
        )


class MetasTQISerializer(serializers.ModelSerializer):

    class Meta:
        model = MetasTQI
        fields = (
            'contrato',
            'anio',
            'mes',
            'cantidad_meta',
            'cantidad_programada',
            'cantidad_ejecutada',
            'fecha_actualizacion',
            'responsable_actualizacion',
        )


class MetasTQIContratoSerializer(serializers.Serializer):

    contrato = ContratoSerializer()
    total_meta = serializers.IntegerField()
    total_programada = serializers.IntegerField()
    total_ejecutada = serializers.IntegerField()


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

class MetasInspectoresTotalesSerializer(serializers.Serializer):

    inspector = UserSerializer()
    total_meta = serializers.IntegerField()
    total_programada = serializers.IntegerField()
    total_ejecutada = serializers.IntegerField()

   

class PdlTqiPagination(pagination.PageNumberPagination):
    page_size = 20
    max_page_size = 100