from rest_framework import serializers
from ..models.estructura_presupuestal import EstructuraPresupuestal

# proceso (Deuda técnica, optimizar los campos que requiero por vista)

class EstructuraPresupuestalSerializer(serializers.ModelSerializer):
    class Meta:
        model=EstructuraPresupuestal
        fields=('__all__')