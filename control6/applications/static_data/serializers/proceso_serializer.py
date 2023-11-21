from rest_framework import serializers
from ..models.proceso import Proceso

# proceso (Deuda técnica, optimizar los campos que requiero por vista)

class ProcesoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Proceso
        fields=('__all__')

    
class ConteoProcesoSerializer(serializers.Serializer):
    proceso=serializers.CharField()
    cantidad=serializers.IntegerField()