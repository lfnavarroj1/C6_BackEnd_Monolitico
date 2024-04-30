from django.db import models
# from django.db.models import Q
from ..users_management.models import User
from ..odm_management.models import Odm
from rest_framework.response import Response
from ..scheduling_management.models import Programacion


class ManiobraManager(models.Manager):
    def registrar_maniobra(self,req):
        datos={}
        datos["maniobra"]=req["maniobra"]
        datos["tipo_maniobra"]=req["tipo_maniobra"]
        datos["alcance"]=req["alcance"]
        datos["fecha_inicio"]=req["fecha_inicio"]
        datos["fecha_fin"]=req["fecha_fin"]
        datos["estado_maniobra"]=req["estado_maniobra"]

        maniobra=self.create(**datos) # Falta implementar manejo de excepciones
        lista_programaciones=list(map(str,req["programaciones"].split(',')))
        maniobra.programaciones.set(Programacion.objects.filter(pk__in=lista_programaciones))
        return Response({'message': f'La {maniobra} fue agregada con éxito'}, status=201)
    
    def obtener_maniobras(self,id_control):
        result=self.filter(programaciones__lcls__odms__valorizacion__trabajo__id_control=id_control).distinct()
        return result
    

    def actualizar_maniobra(self, maniobra_data,maniobra):
        maniobra_actual=self.get(pk=maniobra)

        campos_actualizables=[
            "programaciones",
            "tipo_maniobra",
            "alcance",
            "fecha_inicio",
            "fecha_fin",
            "estado_maniobra",
        ]

        # CAMPOS RELACIONADOS
        for campo in campos_actualizables:
            if campo in maniobra_data:

                if campo=="programaciones":
                    lista_programaciones=list(map(str,maniobra_data["programaciones"].split(',')))
                    maniobra_actual.programaciones.set(Programacion.objects.filter(pk__in=lista_programaciones))
                else:
                    setattr(maniobra_actual,campo,maniobra_data[campo])
        
        maniobra_actual.save()
        return maniobra_actual