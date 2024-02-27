from rest_framework import serializers

from ..models.programacion import Programacion

class ProgramacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programacion
        fields = (
            "id_programcion",
            'trabajo',
            "fecha_ejecucion",
            "cuadrillas",
            "lcls",
            "alcance",
            "estado",
            "observacion",
            "ticket",
            "pdl",
            "pi",
            "pstl",
            "vyp",
            "planeacion_segura",
        )