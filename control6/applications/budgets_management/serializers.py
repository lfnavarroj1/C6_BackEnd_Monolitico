# from rest_framework import serializers
# from .models import (
#     Valorizacion, 
#     Nodo, 
#     NodoMDO, 
#     NodoMAT,
#     EtlBudget
# )

# class ValorizacionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Valorizacion
#         fields = (
#             "id_valorizacion",
#             "trabajo",
#             "monto_mano_obra",
#             "monto_materiales",
#             "fecha_valorizacion",
#             "estado",
#             "nivel_tension",
#             "presupuesto",
#         )

# class NodoSerializer( serializers.ModelSerializer ):
#     class Meta:
#         model = Nodo
#         fields = (
#             "id_nodo",
#             "valorizacion",
#             "nodo",
#             "latitud_inicial",
#             "longitud_inicial",
#             "latitud_final",
#             "longitud_final",
#             "punto_fisico_final",
#             "punto_fisico_inicial",
#             "norma_codensa_punto_inicial",
#             "norma_codensa_punto_final",
#             "tipo_nodo",
#             "tipo_instalacion",
#             "nivel_tension",
#             "tramo",
#             "cod_seccion",
#             "cod_defecto",
#             "valor_mano_obra",
#             "valor_materiales",
#             "id_mare",
#         )

# class CrearNodoRG12Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = Nodo
#         fields = (
#             "id_nodo",
#             "valorizacion",
#             "nodo",
#             "latitud_inicial",
#             "longitud_inicial",
#             "punto_fisico_inicial",
#             "norma_codensa_punto_inicial",
#             "nivel_tesion",
#             "tramo",
#             "cod_seccion",
#             "cod_defecto",
#             "id_mare",
#         )

# class CrearNodoRG10Serializer(serializers.ModelSerializer):
#     class Meta:
#         model = Nodo
#         fields = (
#             "id_nodo",
#             "valorizacion",
#             "nodo",
#             "latitud_inicial",
#             "longitud_inicial",
#             "punto_fisico_inicial",
#         )

# class NodoMDOSerializer( serializers.ModelSerializer ):
#     class Meta:
#         model = NodoMDO
#         fields = (
#             "nodo",
#             "tipo_trabajo_mdo",
#             "codigo_mdo",
#             "cantidad_replanteada",
#             "cantidad_ejecutada",
#             "cantidad_facturada"
#         )

# class NodoMATerializer( serializers.ModelSerializer ):
#     class Meta:
#         model = NodoMAT
#         fields = (
#             "nodo",
#             "tipo_trabajo_mat",
#             "codigo_mat",
#             "cantidad_replanteada",
#             "cantidad_ejecutada",
#             "cantidad_facturada",
#             "aportacion",
#         )

# class EtlBudgetSerializer( serializers.ModelSerializer ):
#     class Meta:
#         model = EtlBudget
#         fields = (
#             "nodo",
#             "instalacion_retiro",
#             "codigo",
#             "cantidad",
#             "mat_mdo",
#             "aportacion",
#         )