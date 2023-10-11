from rest_framework import serializers
from ..models.trazabilidad import Trazabilidad

# proceso (Deuda técnica, optimizar los campos que requiero por vista)

class TrazabilidadSerializer(serializers.ModelSerializer):
    class Meta:
        model=Trazabilidad
        fields=('__all__')
