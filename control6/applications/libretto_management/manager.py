from django.db import models
from static_data.models.nivel_tension import NivelTension
from static_data.models.proceso import Proceso
from static_data.models.estructura_presupuestal import EstructuraPresupuestal
from static_data.models.unidad_territorial import UnidadTerritorial
from static_data.models.municipio import Municipio
from static_data.models.vereda import Vereda
from static_data.models.subestacion import Subestacion
from static_data.models.circuito import Circuito
from static_data.models.contrato import Contrato

from work_management.models.lcl import Lcl

from django.db.models import Q
# from ...users.models import User
import os


class LibretoManager(models.Manager):  
    def actualizar_libreto(self, libreto_data,id_libreto):
        libreto_actual=self.get(pk=id_libreto)
    
        campos_actualizables=[
            "numero_libreto",
            "lcl",
            "valor_mod",
            "valor_mat",
            "observacion",
            "planillas_conciliacion",
            "planillas_firmadas",
            "estado_libreto",
            "es_ultimo_libreto",
        ]

        # CAMPOS RELACIONADOS
        for campo in campos_actualizables:
            if campo in libreto_data:
                if campo=="planillas_conciliacion":
                    if libreto_actual.planillas_conciliacion:
                        file_path=libreto_actual.planillas_conciliacion.path
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    setattr(libreto_actual,"planillas_conciliacion",libreto_data["planillas_conciliacion"])

                elif campo=="planillas_firmadas":
                    if libreto_actual.planillas_firmadas:
                        file_path=libreto_actual.planillas_firmadas.path
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    setattr(libreto_actual,"planillas_firmadas",libreto_data["planillas_firmadas"])
                elif campo=="es_ultimo_libreto":
                    if libreto_data["es_ultimo_libreto"].lower()=="true":
                        setattr(libreto_actual,"es_ultimo_libreto",True)
                    else:
                        setattr(libreto_actual,"es_ultimo_libreto",False)
                elif campo=="lcl" and libreto_data[campo] != "":
                    setattr(libreto_actual, campo, Lcl.objects.filter(lcl=libreto_data[campo]).first())

                else:
                    print(campo)
                    setattr(libreto_actual, campo, libreto_data[campo])


        libreto_actual.save()
        return libreto_actual
