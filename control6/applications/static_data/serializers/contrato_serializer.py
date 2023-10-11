from rest_framework import serializers
from ..models.contrato import Contrato

# proceso (Deuda técnica, optimizar los campos que requiero por vista)

class ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contrato
        fields=('__all__')