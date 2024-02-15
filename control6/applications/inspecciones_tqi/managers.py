from django.db import models
# from ...static_data.models.ruta_proceso import RutaProceso
# from ...static_data.models.proceso import Proceso
# from ...static_data.models.estructura_presupuestal import EstructuraPresupuestal
# from ...static_data.models.unidad_territorial import UnidadTerritorial
# from ...static_data.models.municipio import Municipio
# from ...static_data.models.vereda import Vereda
# from ...static_data.models.subestacion import Subestacion
# from ...static_data.models.circuito import Circuito
# from ...static_data.models.contrato import Contrato
# from ..errores import CampoRequeridoError

from django.db.models import Q
# from ...users.models import User
# from ..serializers.trabajo_serializer import TrabajoSerializer

from django.db.models import Sum


class ManiobrasTQIManager(models.Manager):
    def filtrar_maniobras( self, vector_unidades_territoriales, vector_contratos, vector_estados, vector_anio, vector_meses, kword ):
        print(kword)
        result = self.filter (
            Q( unidad_ejecutora__in = vector_unidades_territoriales ),
            Q( contrato__in = vector_contratos ),
            Q( estado_tqi__in = vector_estados ),
            Q( anio__in = vector_anio ),
            Q( mes__in = vector_meses ),
            Q(codigo__icontains = kword ), #| Q(inspector_asingado__icontains = kword ),
        )
        return result
    
class MetasInspectoresManager(models.Manager):
    def filtrar_inspectores( self, vector_anio, vector_meses ):
        result = self.filter (
            Q( anio__in = vector_anio ),
            Q( mes__in = vector_meses ),
        ).aggregate(
                total_meta=Sum('cantidad_meta'),
                total_programada=Sum('cantidad_programada'),
                total_ejecutada=Sum('cantidad_ejecutada')
        )
        return result
    
    
