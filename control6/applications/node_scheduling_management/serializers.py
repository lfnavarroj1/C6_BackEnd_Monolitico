from rest_framework import serializers
from ..models.nodo_seguimiento import NodoSeguimiento


class NodoSeguimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model=NodoSeguimiento
        fields=(
            "nodo",
            "programacion",
            "programado",
            "ejecutado",
            "facturado",
        )
