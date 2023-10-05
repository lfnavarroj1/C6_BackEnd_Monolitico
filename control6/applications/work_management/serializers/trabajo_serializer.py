from rest_framework import serializers
from ..models.trabajo import Trabajo

# proceso (Deuda técnica, optimizar los campos que requiero por vista)

class TrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Trabajo
        fields=('__all__')


class CrearTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Trabajo
        fields=(
            "pms_quotation",
            "pms_need",
            "proceso",
            "caso_radicado",
            'estado_trabajo',
            "alcance",
            "estructura_presupuestal",
            "priorizacion",
            "unidad_territorial",
            "municipio",
            "vereda",
            "direccion",
            "subestacion",
            "circuito",
            "contrato",
        )