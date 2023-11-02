from rest_framework import serializers
from ..models.programacion import Programacion

class ProgramacionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Programacion
        fields=(
            "id_programcion",
            "fecha_ejecucion",
            "cuadrillas",
            "lcls",
            "alcance",
            "estado",
        )

class CrearProgramacionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Programacion
        fields=(
            "fecha_ejecucion",
            "cuadrillas",
            "lcls",
            "alcance",
            "estado",
        )