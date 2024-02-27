from rest_framework import serializers
from .models import Odm


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
