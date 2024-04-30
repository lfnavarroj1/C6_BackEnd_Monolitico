# from django.db import models
# from ..static_data.models.ruta_proceso import RutaProceso
# from ..static_data.models.proceso import Proceso
# from ..static_data.models.estructura_presupuestal import EstructuraPresupuestal
# from ..static_data.models.unidad_territorial import UnidadTerritorial
# from ..static_data.models.municipio import Municipio
# from ..static_data.models.vereda import Vereda
# from ..static_data.models.subestacion import Subestacion
# from ..static_data.models.circuito import Circuito
# from ..static_data.models.contrato import Contrato
# from .errores import CampoRequeridoError
# from django.db.models import Q

# class TrabajoManager(models.Manager):  
#     def crear_trabajo(self, trabajo_data):
#         campos = [
#             "pms_quotation",
#             "pms_need",
#             "proceso",
#             "caso_radicado",
#             'ruta_proceso',
#             "alcance",
#             "estructura_presupuestal",
#             "priorizacion",
#             "unidad_territorial",
#             "municipio",
#             "vereda",
#             "direccion",
#             "subestacion",
#             "circuito",
#             "contrato",
#             "cantidad",
#         ]
        
#         for campo in campos:
#             if campo in trabajo_data:
#                 if trabajo_data[campo] == "" or trabajo_data[campo] is None:
#                     trabajo_data[campo] = ""
#             else:
#                  trabajo_data[campo] = ""

#         campos_obligatorios = ["proceso", "alcance", "unidad_territorial", "municipio","direccion", "vereda", "subestacion", "circuito", "contrato", "priorizacion", "cantidad"]
#         for campo in campos_obligatorios:
#             if trabajo_data[campo] == "":
#                 return {"message":'Los campo "proceso", "alcance", "unidad_territorial", "municipio", "direccion", "vereda", "subestacion", "circuito", "contrato" y "priorizacion" son obligatorios', "creado_exitosamente": False}
        
#         proceso_id = trabajo_data["proceso"]
#         trabajo_data["proceso"] = Proceso.objects.get(pk=proceso_id)

#         uni_id=trabajo_data["unidad_territorial"]
#         trabajo_data["unidad_territorial"] = UnidadTerritorial.objects.get(pk=uni_id)

#         uni_id=trabajo_data["municipio"]
#         trabajo_data["municipio"] = Municipio.objects.get(pk=uni_id)

#         uni_id=trabajo_data["vereda"]
#         trabajo_data["vereda"] = Vereda.objects.get(pk=uni_id)

#         uni_id= trabajo_data["subestacion"]
#         trabajo_data["subestacion"] = Subestacion.objects.get(pk=uni_id)

#         uni_id=trabajo_data["circuito"]
#         trabajo_data["circuito"] = Circuito.objects.get(pk=uni_id)

#         uni_id=trabajo_data["contrato"]
#         trabajo_data["contrato"] = Contrato.objects.get(pk=uni_id)

#         if trabajo_data["estructura_presupuestal"]!="":
#             uni_id = trabajo_data["estructura_presupuestal"]
#             estructura_presupuestal = EstructuraPresupuestal.objects.filter(pk=uni_id).first()
#             if estructura_presupuestal:
#                 trabajo_data["estructura_presupuestal"] = estructura_presupuestal
#             else:
#                 trabajo_data["estructura_presupuestal"] = None
#         else:
#             trabajo_data["estructura_presupuestal"] = None

#         trabajo_data["ruta_proceso"] = RutaProceso.objects.filter(proceso=trabajo_data["proceso"], paso="1").first()
#         nuevo_trabajo=self.create(**trabajo_data)
#         return {"trabajo": nuevo_trabajo, "creado_exitosamente": True}
    

#     def filtrar_trabajos(self, vprocesos, vestados, kword, user):
#         result = self.filter(
#             Q(proceso__in=vprocesos),
#             Q(unidad_territorial__in = user.unidades_territoriales.all()),
#             Q(contrato__in = user.contratos.all()), 
#             Q(ruta_proceso__estado__id_estado__in=vestados),
#             Q(id_control__icontains = kword ) | Q( caso_radicado__icontains = kword ) | Q( ticket__icontains = kword ),
#         )
#         return result
    

#     def obtener_detalle_trabajo(self, id_control):
#         return self.filter(id_control=id_control).first()


#     def actualizar_trabajo(self, trabajo_data, id_control):
#         trabajo_actualizado = self.filter(pk=id_control).first()

#         if trabajo_actualizado:

#             campos_actualizables = [
#                 "pms_quotation",
#                 "pms_need",
#                 "caso_radicado",
#                 "ruta_proceso",
#                 "alcance",
#                 "estructura_presupuestal",
#                 "priorizacion",
#                 "unidad_territorial",
#                 "municipio",
#                 "vereda",
#                 "direccion",
#                 "subestacion",
#                 "circuito",
#                 "contrato",
#                 "ticket",
#                 "equipo_referencia",
#                 "carga_solicitada",
#                 "cantidad",
#             ]

#             for campo in campos_actualizables:
#                 if campo in trabajo_data:

#                     if campo=="unidad_territorial":
#                         setattr(trabajo_actualizado,"unidad_territorial",UnidadTerritorial.objects.get(pk=trabajo_data["unidad_territorial"]))

#                     elif campo=="municipio":
#                         setattr(trabajo_actualizado,"municipio", Municipio.objects.get(pk=trabajo_data["municipio"]))

#                     elif campo=="vereda":
#                         setattr(trabajo_actualizado,"vereda", Vereda.objects.get(pk=trabajo_data["vereda"]))

#                     elif campo=="subestacion":
#                         setattr(trabajo_actualizado,"subestacion", Subestacion.objects.get(pk=trabajo_data["subestacion"]))

#                     elif campo=="circuito":
#                         setattr(trabajo_actualizado,"circuito", Circuito.objects.get(pk=trabajo_data["circuito"]))

#                     elif campo=="contrato":
#                         setattr(trabajo_actualizado,"contrato", Contrato.objects.get(pk=trabajo_data["contrato"]))

#                     elif campo=="estructura_presupuestal":
#                         setattr(trabajo_actualizado,"estructura_presupuestal", EstructuraPresupuestal.objects.get(pk=trabajo_data["estructura_presupuestal"]))
#                     else:
#                         setattr(trabajo_actualizado, campo, trabajo_data[campo])

#             trabajo_actualizado.save()
#             return {"work": trabajo_actualizado, "work_exist": True}
        
#         return {"work_exist": False}


#     def lista_trabajos( self ):
#         result = self.all()
#         return result
    
    
    