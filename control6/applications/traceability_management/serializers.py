from rest_framework import serializers
from .models import TrazabilidadTrabajo, TrazabilidadInspeccionesTqi
from ..users_management.serializers import UserSerializer

class TrazabilidadTrabajoSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    class Meta:
        model = TrazabilidadTrabajo
        fields = (
                'trabajo',
                'usuario',
                'fecha_trazabilidad',
                'comentario_trazabilidad',
            )
        
class TrazabilidadInspeccionesTqiSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    class Meta:
        model = TrazabilidadInspeccionesTqi
        fields = (
                'maniobra',
                'usuario',
                'fecha_trazabilidad',
                'comentario_trazabilidad',
            )