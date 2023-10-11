from django.db import models
from ...static_data.models.ruta_proceso import RutaProceso
from ...static_data.models.proceso import Proceso
from ...static_data.models.estructura_presupuestal import EstructuraPresupuestal
from ...static_data.models.unidad_territorial import UnidadTerritorial
from ...static_data.models.municipio import Municipio
from ...static_data.models.vereda import Vereda
from ...static_data.models.subestacion import Subestacion
from ...static_data.models.circuito import Circuito
from ...static_data.models.contrato import Contrato
from ..errores import CampoRequeridoError

# from django.db.models import Q
# from ...users.models import User


class TrabajoManager(models.Manager):  
    # 1. LISTAR TRABAJOS
    def lista_trabajos(self):
        result=self.all()
        return result
    
    def crear_trabajo(self, trabajo_data):
        # CREAR UN NUEVO TRABAJO
        # 1. Recibir y validar los datos de la petición
        campos=[
            "pms_quotation", # No requerido
            "pms_need", # No requerido
            "proceso", # requerido
            "caso_radicado",
            'ruta_proceso',
            "alcance",
            "estructura_presupuestal",
            "priorizacion",
            "unidad_territorial",
            "municipio",
            "vereda",
            "direccion",
            "subestacion",
            "circuito",
            "contrato",
            ]
        for campo in campos:
            if campo in trabajo_data:
                if trabajo_data[campo]=="" or trabajo_data[campo] is None:
                    trabajo_data[campo]=""
            else:
                 trabajo_data[campo]=""
        
        # CAMPOS OBLIGATORIOS
        campos_obligatorios=["proceso", "alcance", "unidad_territorial", "municipio","direccion", "vereda", "subestacion", "circuito", "contrato"]
        for campo in campos_obligatorios:
            if trabajo_data[campo]=="":
                raise CampoRequeridoError(campo)
        
        proceso_id=trabajo_data["proceso"]
        trabajo_data["proceso"]=Proceso.objects.get(pk=proceso_id)

        uni_id=trabajo_data["unidad_territorial"]
        trabajo_data["unidad_territorial"]=UnidadTerritorial.objects.get(pk=uni_id)

        uni_id=trabajo_data["municipio"]
        trabajo_data["municipio"]=Municipio.objects.get(pk=uni_id)

        uni_id=trabajo_data["vereda"]
        trabajo_data["vereda"]=Vereda.objects.get(pk=uni_id)

        uni_id= trabajo_data["subestacion"]
        trabajo_data["subestacion"]=Subestacion.objects.get(pk=uni_id)

        uni_id=trabajo_data["circuito"]
        trabajo_data["circuito"]=Circuito.objects.get(pk=uni_id)

        uni_id=trabajo_data["contrato"]
        trabajo_data["contrato"]=Contrato.objects.get(pk=uni_id)

        # CAMPO REFERENCIAL OPCIONAL
        if trabajo_data["estructura_presupuestal"]!="":
            uni_id=trabajo_data["estructura_presupuestal"]
            trabajo_data["estructura_presupuestal"]=EstructuraPresupuestal.objects.get(pk=uni_id)
        else:
            trabajo_data["estructura_presupuestal"]=None

        # 2. Asignar lo valores por defecto de la creación
        trabajo_data["ruta_proceso"]=RutaProceso.objects.filter(proceso=trabajo_data["proceso"], paso="1").first()

        # 3. Crear el trabajo con los datos suministrados
        nuevo_trabajo=self.create(**trabajo_data)

        # 5. Devolver el resultado de la creación.
        return nuevo_trabajo
    
    def actualizar_trabajo(self, trabajo_data,id_control):
        # ACTUALIZAR UN TRABAJO

        # 2. FILTRAR EL TRABAJO A MODIFICAR
        trabajo_actualizado=self.get(pk=id_control)

        campos_actualizables=[
            "pms_quotation",
            "pms_need",
            "ruta_proceso",
            "caso_radicado",
            "alcance",
            "estructura_presupuestal",
            "priorizacion",
            "unidad_territorial",
            "municipio",
            "vereda",
            "direccion",
            "subestacion",
            "circuito",
            "contrato",
        ]

        # CAMPOS RELACIONADOS
        for campo in campos_actualizables:
            if campo in trabajo_data:

                if campo=="unidad_territorial":
                    setattr(trabajo_actualizado,"unidad_territorial",UnidadTerritorial.objects.get(pk=trabajo_data["unidad_territorial"]))

                elif "municipio" in trabajo_data:
                    setattr(trabajo_actualizado,"municipio", Municipio.objects.get(pk=trabajo_data["municipio"]))

                elif "vereda" in trabajo_data:
                    setattr(trabajo_actualizado,"vereda", Vereda.objects.get(pk=trabajo_data["vereda"]))

                elif "subestacion" in trabajo_data:
                    setattr(trabajo_actualizado,"subestacion", Subestacion.objects.get(pk=trabajo_data["subestacion"]))

                elif "circuito" in trabajo_data:
                    setattr(trabajo_actualizado,"circuito",Circuito.objects.get(pk=trabajo_data["circuito"]))

                elif "contrato" in trabajo_data:
                    setattr(trabajo_actualizado,"contrato",Contrato.objects.get(pk=trabajo_data["contrato"]))

                elif "estructura_presupuestal" in trabajo_data:
                    setattr(trabajo_actualizado,"estructura_presupuestal",EstructuraPresupuestal.objects.get(pk=trabajo_data["estructura_presupuestal"]))
                else:
                    setattr(trabajo_actualizado,campo,trabajo_data[campo])

        trabajo_actualizado.save()
        return trabajo_actualizado



#  # Buscar Trabajos
#     def lista_trabajos(self):
#         # a . Procesos asociados al usuario
#         if procesos:
#             print("Algo")
#         else:
#             procesos=User.objects.get(id=user.id).process.all()

#         # Estados asociado al usuario.

#         if not(estados):
#             estados=User.objects.get(id=user.id).state_works.all()

#         # b. Filtro con las condiciones 
#         result=self.filter(
#             Q(proceso__in=procesos),
#             Q(estado_trabajo__in=estados),
#             Q(pms_quotation__icontains=kword) | Q(caso_radicado__icontains=kword),
#             )
#         return result
    
#     # Listar procesos de un usuario
#     def lista_procesos_usuario(self,user):
#         procesos=User.objects.get(id=user.id).process.all()
#         return procesos
    
#     def lista_estado_usuario(self,user):
#         estados=User.objects.get(id=user.id).state_works.all()
#         return estados

# class TrazabilidadManager(models.Manager):

#     def agregar_trazabilidad(self,mensaje):
#         traza=self()
#         traza.save()
        

    
    
