from rest_framework import serializers
from ..models.trazabilidad import Trazabilidad
from ...users.serializers import UserSerializer

# proceso (Deuda técnica, optimizar los campos que requiero por vista)

class TrazabilidadSerializer(serializers.ModelSerializer):
    usuario=UserSerializer()
    class Meta:
        model=Trazabilidad
        fields=(
            'trabajo',
            'usuario',
            'fecha_trazabilidad',
            'comentario_trazabilidad',
            )
