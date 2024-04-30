# from rest_framework import serializers
# from .models import User #, C6Modules
# # from ..static_data.models.proceso import Proceso
# # from ..static_data.models.estado_trabajo import EstadoTrabajo
# # from ..static_data.serializers.unidad_territorial_serializer import UnidadTerritorialSerializer
# # from ..static_data.serializers.contrato_serializer import ContratoSerializer

# # class C6ModulesSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = C6Modules
# #         fields = ('__all__')

# # class ProcesoUserSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Proceso
# #         fields = ('__all__')

# # class EstadoUserSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = EstadoTrabajo
# #         fields = ('__all__')

# class UserSerializer(serializers.ModelSerializer):
#     # procesos = ProcesoUserSerializer(many=True)
#     # user_modules = C6ModulesSerializer(many=True)
#     # estado_trabajo = EstadoUserSerializer(many=True)
#     # unidades_territoriales = UnidadTerritorialSerializer(many=True)
#     # contratos = ContratoSerializer(many=True)

#     class Meta:
#         model=User
#         fields = ('__all__')
#         extra_kwargs = {'password':{'write_only':True}}
    
#     def create(self,validated_data):
#         password = validated_data.pop('password', None)
#         instance = self.Meta.model(**validated_data)
#         if password is not None:
#             instance.set_password(password)
        
#         instance.save()
#         return instance
    
# class UserCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'password',
#             'assigned'
#         )
#         extra_kwargs = {'password':{'write_only':True}}
    
#     def create(self, validated_data):
#         password = validated_data.pop('password', None)
#         instance=self.Meta.model(**validated_data)
#         if password is not None:
#             instance.set_password(password)
        
#         instance.save()
#         return instance


# class ChangePasswordSerializer(serializers.Serializer):
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)