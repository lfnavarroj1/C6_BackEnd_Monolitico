from rest_framework import serializers
from ..models.valorizacion import Valorizacion


class ValorizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Valorizacion
        fields=(
            "id_valorizacion",
            "trabajo",
            "monto_mano_obra",
            "monto_materiales",
            "estado",
            "nivel_tension",
            "presupuesto",
        )

class CrearValorizacion(serializers.ModelSerializer):
    class Meta:
        model=Valorizacion
        fields=(
            "trabajo",
            "monto_mano_obra",
            "monto_materiales",
            "estado",
            "nivel_tension",
            "presupuesto",
        )