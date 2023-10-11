from rest_framework import serializers
from ..models.vereda import Vereda

# proceso (Deuda técnica, optimizar los campos que requiero por vista)

class VeredaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vereda
        fields=('__all__')