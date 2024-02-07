from rest_framework import serializers
from ..models.trabajo import Trabajo
from ...static_data.serializers.proceso_serializer import ProcesoSerializer
from ...static_data.serializers.ruta_proceso_serializer import RutaProcesoSerializer
from ...static_data.serializers.estructura_presupuestal_serializer import EstructuraPresupuestalSerializer
from ...static_data.serializers.unidad_territorial_serializer import UnidadTerritorialSerializer
from ...static_data.serializers.municipio_serializer import MunicipioSerializer
from ...static_data.serializers.vereda_serializer import VeredaSerializer
from ...static_data.serializers.subestacion_serializer import SubestacionSerializer
from ...static_data.serializers.circuito_serializer import CircuitoSerializer
from ...static_data.serializers.contrato_serializer import ContratoSerializer

# proceso (Deuda técnica, optimizar los campos que requiero por vista)

class TrabajoSerializer(serializers.ModelSerializer):
    proceso=ProcesoSerializer()
    ruta_proceso=RutaProcesoSerializer()
    estructura_presupuestal=EstructuraPresupuestalSerializer()
    unidad_territorial=UnidadTerritorialSerializer()
    municipio=MunicipioSerializer()
    vereda=VeredaSerializer()
    subestacion=SubestacionSerializer()
    circuito=CircuitoSerializer()
    contrato=ContratoSerializer()
    
    class Meta:
        model=Trabajo
        fields=(
            'id_control',
            'pms_quotation',
            'pms_need',
            'proceso',
            'ruta_proceso',
            'caso_radicado',
            'alcance',
            'estructura_presupuestal',
            'priorizacion',
            'unidad_territorial',
            'municipio',
            'vereda',
            'direccion',
            'subestacion',
            'circuito',
            'equipo_referencia',
            'carga_solicitada',
            'contrato',
            'ticket',
            'cantidad',

        )


class CrearTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Trabajo
        fields=(
            "pms_quotation",
            "pms_need",
            "proceso",
            "caso_radicado",
            'ruta_proceso',
            "alcance",
            "estructura_presupuestal",
            "priorizacion",
            "unidad_territorial",
            "municipio",
            "vereda",
            "direccion",
            "subestacion",
            "circuito",
            "contrato",
        )