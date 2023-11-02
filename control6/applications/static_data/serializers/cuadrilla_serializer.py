from rest_framework import serializers
from ..models.cuadrilla import Cuadrilla

# Serializando las cuadrillas

class CuadrillaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cuadrilla
        fields=('__all__')