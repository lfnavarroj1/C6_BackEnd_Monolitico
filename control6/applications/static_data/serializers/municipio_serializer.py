from rest_framework import serializers
from ..models.municipio import Municipio

# proceso (Deuda técnica, optimizar los campos que requiero por vista)

class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model=Municipio
        fields=('__all__')