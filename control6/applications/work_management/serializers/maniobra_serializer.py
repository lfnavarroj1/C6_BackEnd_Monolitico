from rest_framework import serializers
from ..models.maniobra import Maniobra


class ManiobraSerializer(serializers.ModelSerializer):
    class Meta:
        model=Maniobra
        fields=(
            "mabiobra",
            "programacion",
            "tipo_maniobra",
            "alcance",
            "fecha_inicio",
            "fecha_fin",
            "estado_maniobra",
        )
