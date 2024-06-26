from django.db import models
# from django.db.models import Q
from ..users_management.models import User
from ..odm_management.models import Odm
from rest_framework.response import Response
from django.db.models import Q

class LclManager(models.Manager):
    def agregar_lcl(self, req, user):
        datos = {}
        datos["lcl"] = req["lcl"]
        datos["estado_lcl"] = req["estado_lcl"]
        datos["indicador_impuesto"] = req["indicador_impuesto"]
        datos["valor_mano_obra"] = req["valor_mano_obra"]
        datos["valor_materiales"] = req["valor_materiales"]
        datos["responsable_scm"] = user
        datos["texto_scm"] = "None" # <-- Texto para SCM, crearlo.
        datos["alcance"] = req["alcance"]

        lcl = self.create(**datos) # Falta implementar manejo de excepciones

        lista_odm=list(map(int,req["odms"].split(',')))
        lcl.odms.set(Odm.objects.filter(pk__in=lista_odm))

        return Response({'message': f'La {lcl} fue agregada con éxito'}, status=201)

    def filtrar_lcl(self,vprocesos,vestados,kword):

        result=self.filter(
            Q(odms__valorizacion__trabajo__proceso__in=vprocesos),
            Q(estado_lcl__in=vestados),
            Q(lcl__icontains=kword),
            )
        return set(result)

    def contar_lcl_procesos(self,vprocesos,vestados,kword):
        result=self.filter(
            
        Q(proceso__in=vprocesos),
        Q(ruta_proceso__estado__id_estado__in=vestados),
        Q(id_control__icontains=kword) | Q(caso_radicado__icontains=kword) | Q(ticket__icontains=kword),
        )
        return result



    def obtener_lcls(self,id_control):
        result=self.filter(odms__valorizacion__trabajo__id_control=id_control).distinct()
        return result
    

    def actualizar_lcl(self, lcl_data,lcl):
        lcl_actual=self.get(pk=lcl)

        campos_actualizables=[
            "estado_lcl",
            "indicador_impuesto",
            "valor_mano_obra",
            "valor_materiales",
            "texto_scm",
            "alcance",
            "odms",
        ]

        # CAMPOS RELACIONADOS
        for campo in campos_actualizables:
            if campo in lcl_data:
                if campo=="odms":
                    lista_odm=list(map(int,lcl_data["odms"].split(',')))
                    lcl_actual.odms.set(Odm.objects.filter(pk__in=lista_odm))
                elif campo=="responsable_scm":
                    setattr(lcl_actual,campo,User.objects.get(pk=lcl_data["responsable_scm"]))
                else:
                    setattr(lcl_actual,campo,lcl_data[campo])
        
        lcl_actual.save()
        return lcl_actual
    

