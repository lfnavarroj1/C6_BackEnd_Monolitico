from rest_framework import serializers
from ..models.subestacion import Subestacion

# proceso (Deuda técnica, optimizar los campos que requiero por vista)

class SubestacionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subestacion
        fields=('__all__')