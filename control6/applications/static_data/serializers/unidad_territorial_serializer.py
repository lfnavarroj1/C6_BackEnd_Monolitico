from rest_framework import serializers
from ..models.unidad_territorial import UnidadTerritorial

# proceso (Deuda técnica, optimizar los campos que requiero por vista)

class UnidadTerritorialSerializer(serializers.ModelSerializer):
    class Meta:
        model=UnidadTerritorial
        fields=('__all__')