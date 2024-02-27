from rest_framework import serializers
from .models import Lcl


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

class LclListaSerializer(serializers.ModelSerializer):
    proceso = serializers.SerializerMethodField()
    id_control=serializers.SerializerMethodField()
    class Meta:
        model=Lcl
        fields=(
            "lcl",
            "proceso",
            "id_control",
            "indicador_impuesto",
            "valor_mano_obra",
            "valor_materiales",
            "estado_lcl",

        )
    
    def get_proceso(self,obj):
        return set(list(obj.odms.values_list("valorizacion__trabajo__proceso__nombre", flat=True)))
    
    def get_id_control(self,obj):
        return set(list(obj.odms.values_list("valorizacion__trabajo__id_control", flat=True)))