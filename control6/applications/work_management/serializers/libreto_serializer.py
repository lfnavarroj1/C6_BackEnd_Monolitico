from rest_framework import serializers
from ..models.libreto import Libreto


class LibretoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Libreto
        fields=(
            "id_libreto",
            "programacion",
            "lcl",
            "numero_libreto",
            "valor_mod",
            "valor_mat",
            "observacion",
            "planillas_conciliacion",
            "planillas_firmadas",
            "estado_libreto",
            "es_ultimo_libreto",
            "trabajo",
        )

class CrearLibretoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Libreto
        fields=(
            "programacion",
            "lcl",
            "numero_libreto",
            "valor_mod",
            "valor_mat",
            "observacion",
            "planillas_conciliacion",
            "planillas_firmadas",
            "estado_libreto",
            "es_ultimo_libreto",
            "trabajo",
        )