from rest_framework import serializers
from ..models.proceso import Proceso
from ..models.contrato import Contrato
from ..models.unidad_territorial import UnidadTerritorial
from ..models.municipio import Municipio
from ..models.vereda import Vereda
from ..models.subestacion import Subestacion 
from ..models.circuito import Circuito

# proceso (Deuda técnica, optimizar los campos que requiero por vista)

class ProcesoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Proceso
        fields=('__all__')

class ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Contrato
        fields=('__all__')

class UnidadTerritorialSerializer(serializers.ModelSerializer):
    class Meta:
        model=UnidadTerritorial
        fields=('__all__')

# municipio
class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model=Municipio
        fields=('__all__')

# vereda
class VeredaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vereda
        fields=('__all__')

# subestacion
class SubestacionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subestacion
        fields=('__all__')

# circuito
class CircuitoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Circuito
        fields=('__all__')
