from rest_framework import serializers
from ..models.lcl import Lcl


class LclSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lcl
        fields=(
            "lcl",
            "estado_lcl",
            "indicador_impuesto",
            "valor_mano_obra",
            "valor_materiales",
            "responsable_scm",
            "texto_scm",
            "alcance",
            "odms",
        )
