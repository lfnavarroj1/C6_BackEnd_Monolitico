from rest_framework import serializers
from ..models.trabajo import Trabajo
from ...static_data.models.proceso import Proceso
from ...static_data.models.municipio import Municipio
from ...static_data.models.vereda import Vereda
from ...static_data.models.subestacion import Subestacion
from ...static_data.models.circuito import Circuito
from ...static_data.models.estado_trabajo import EstadoTrabajo

# proceso (Deuda técnica, optimizar los campos que requiero por vista)

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model=Proceso
        fields=('__all__')

# municipio
class MunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model=Municipio
        fields=('__all__')

# vereda
class VeredaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vereda
        fields=('__all__')

# subestacion
class SubestacionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subestacion
        fields=('__all__')

# circuito
class CircuitoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Circuito
        fields=('__all__')

# estado_trabajo
class EstadoTrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model=EstadoTrabajo
        fields=('__all__')

class TrabajoSerializer(serializers.ModelSerializer):
    proceso=ProcessSerializer()
    municipio=MunicipioSerializer()
    vereda=VeredaSerializer()
    subestacion=SubestacionSerializer()
    circuito=CircuitoSerializer()
    estado_trabajo=EstadoTrabajoSerializer()
    class Meta:
        model=Trabajo
        fields=('__all__')

class CreateWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model=Trabajo
        fields=(
            "pms_quotation",
            "pms_need",
            "proceso",
            "caso_radicado",
            "municipio",
            "vereda",
            "subestacion",
            "circuito",
            "alcance",
            "priorizacion",
            "estado_trabajo",
            "estructura_presupuestal"
        )