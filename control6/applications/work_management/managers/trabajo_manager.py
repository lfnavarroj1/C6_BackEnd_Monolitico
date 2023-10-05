from django.db import models
from django.db.models import Q
#
from ...users.models import User


class TrabajoManager(models.Manager):  
    # 1. LISTAR TRABAJOS
    def lista_trabajos(self):
        result=self.all()
        return result

    
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
        

    
    
