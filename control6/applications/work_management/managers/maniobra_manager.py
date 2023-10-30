from django.db import models
# from django.db.models import Q
from ...users.models import User
from ..models.odm import Odm
from rest_framework.response import Response
from ..models.programacion import Programacion


class ManiobraManager(models.Manager):
    def registrar_maniobra(self,req):
        datos={}
        datos["mabiobra"]=req["mabiobra"]
        datos["programacion"]=Programacion.objects.get(pk=req["programacion"])
        datos["tipo_maniobra"]=req["tipo_maniobra"]
        datos["alcance"]=req["alcance"]
        datos["fecha_inicio"]=req["fecha_inicio"]
        datos["fecha_fin"]=req["fecha_fin"]
        datos["estado_maniobra"]=req["estado_maniobra"]

        maniobra=self.create(**datos) # Falta implementar manejo de excepciones
        # lcl.odms.set(Odm.objects.filter(pk__in=req["odms"]))

        return Response({'message': f'La {maniobra} fue agregada con éxito'}, status=201)
    
    def obtener_maniobras(self,id_control):
        result=self.filter(programacion__lcl__odms__valorizacion__trabajo__id_control=id_control).distinct()
        return result
    

    def actualizar_maniobra(self, maniobra_data,maniobra):
        maniobra_actual=self.get(pk=maniobra)

        campos_actualizables=[
            "programacion",
            "tipo_maniobra",
            "alcance",
            "fecha_inicio",
            "fecha_fin",
            "estado_maniobra",
        ]

        # CAMPOS RELACIONADOS
        for campo in campos_actualizables:
            if campo in maniobra_data:
                if campo=="programacion":
                    setattr(maniobra_actual,campo,Programacion.objects.get(pk=maniobra_data["programacion"]))
                else:
                    setattr(maniobra_actual,campo,maniobra_data[campo])
        
        maniobra_actual.save()
        return maniobra_actual