from rest_framework import serializers
from ..models.estado_trabajo import EstadoTrabajo

# proceso (Deuda técnica, optimizar los campos que requiero por vista)

class EstadoTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model=EstadoTrabajo
        fields=('__all__')