from rest_framework import serializers
from .models import TrazabilidadTrabajo
from ..users.serializers import UserSerializer

# proceso (Deuda técnica, optimizar los campos que requiero por vista)

class TrazabilidadSerializer(serializers.ModelSerializer):
    usuario=UserSerializer()
    class Meta:
        model=TrazabilidadTrabajo
        fields=(
            'trabajo',
            'usuario',
            'fecha_trazabilidad',
            'comentario_trazabilidad',
            )