from rest_framework import serializers
from ..models.valorizacion import Valorizacion, Nodo, NodoMDO, NodoMAT


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
            "id_valorizacion",
            "trabajo",
            "monto_mano_obra",
            "monto_materiales",
            "estado",
            "nivel_tension",
            "presupuesto",
        )

class CrearNodoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Nodo
        fields=(
            "id_nodo",
            "valorizacion",
            "nodo",
            "latitud_inicial",
            "longitud_inicial",
            "latitud_final",
            "longitud_final",
            "punto_fisico_inicial",
            "punto_fisico_final",
            "norma_codensa_punto_inicial",
            "norma_codensa_punto_final",
            "tipo_nodo",
            "tipo_instalacion",
            "nivel_tesion",
        )

class CrearNodoRG12Serializer(serializers.ModelSerializer):
    class Meta:
        model=Nodo
        fields=(
            "id_nodo",
            "valorizacion",
            "nodo",
            "latitud_inicial",
            "longitud_inicial",
            "punto_fisico_inicial",
            "norma_codensa_punto_inicial",
            "nivel_tesion",
            "tramo",
            "cod_seccion",
            "cod_defecto",
            "id_mare",
        )

class CrearNodoRG10Serializer(serializers.ModelSerializer):
    class Meta:
        model=Nodo
        fields=(
            "id_nodo",
            "valorizacion",
            "nodo",
            "latitud_inicial",
            "longitud_inicial",
            "punto_fisico_inicial",
        )

class CrearNodoMDOSerializer(serializers.ModelSerializer):
    class Meta:
        model=NodoMDO
        fields=(
            "nodo",
            "tipo_trabajo_mdo",
            "codigo_mdo",
            "cantidad",
        )

class CrearNodoMATerializer(serializers.ModelSerializer):
    class Meta:
        model=NodoMAT
        fields=(
            "nodo",
            "tipo_trabajo_mat",
            "codigo_mat",
            "cantidad",
        )