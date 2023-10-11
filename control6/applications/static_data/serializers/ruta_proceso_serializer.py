from rest_framework import serializers
from ..models.ruta_proceso import RutaProceso,ModuloBandeja
from ...static_data.serializers.estado_trabajo_serializer import EstadoTrabajoSerializer

class ModuloBandejaSerializer(serializers.ModelSerializer):
    class Meta:
        model=ModuloBandeja
        fields=('__all__')

class RutaProcesoSerializer(serializers.ModelSerializer):
    modulos=ModuloBandejaSerializer(many=True)
    estado=EstadoTrabajoSerializer()
    class Meta:
        model=RutaProceso
        fields=(
            'codigo_ruta',
            'proceso', # Toca serializar con ProcesoSerializars
            'modulos',
            'paso',
            'estado',
            )