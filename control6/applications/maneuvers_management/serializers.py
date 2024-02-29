from rest_framework import serializers
from .models import Maniobra


class ManiobraSerializer(serializers.ModelSerializer):
    class Meta:
        model=Maniobra
        fields=(
            "maniobra",
            "programaciones",
            "tipo_maniobra",
            "alcance",
            "fecha_inicio",
            "fecha_fin",
            "estado_maniobra",
        )
