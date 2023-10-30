from rest_framework import serializers
from ..models.odm import Odm


class OdmSerializer(serializers.ModelSerializer):
    class Meta:
        model=Odm
        fields=(
            "odm",
            "valorizacion",
            "agp",
            "protocolo",
            "solicitud",
        )
