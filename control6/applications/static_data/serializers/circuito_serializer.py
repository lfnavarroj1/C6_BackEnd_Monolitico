from rest_framework import serializers
from ..models.circuito import Circuito

# proceso (Deuda técnica, optimizar los campos que requiero por vista)

class CircuitoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Circuito
        fields=('__all__')