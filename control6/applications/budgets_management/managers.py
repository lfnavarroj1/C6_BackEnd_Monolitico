from django.db import models
from ..static_data.models.nivel_tension import NivelTension
import os

class ValorizacionManager(models.Manager):
    def actualizar_valorizacion(self, valorizacion_data,id_valorizacion):
        valorizacion_actual = self.get(pk=id_valorizacion)
        campos_actualizables = [
            "monto_mano_obra",
            "monto_materiales",
            "estado",
            "nivel_tension",
            "presupuesto",
        ]

        for campo in campos_actualizables:
            if campo in valorizacion_data:
                if campo == "nivel_tension":
                    setattr(valorizacion_actual,"nivel_tension", NivelTension.objects.get(pk=valorizacion_data["nivel_tension"]))
                elif campo == "presupuesto":
                    if valorizacion_actual.presupuesto:
                        file_path = valorizacion_actual.presupuesto.path
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    setattr(valorizacion_actual, campo, valorizacion_data["presupuesto"])         
                else:
                    setattr(valorizacion_actual, campo, valorizacion_data[campo])

        valorizacion_actual.save()
        return valorizacion_actual