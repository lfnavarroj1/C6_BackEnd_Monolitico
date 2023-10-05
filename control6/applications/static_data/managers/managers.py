from django.db import models
# from django.db.models import Q,Count

#
class NivelTensionManager(models.Manager):
    def get_nivel_tesnion(self):
        result=self.all()
        return result






# class ProcesoManager(models.Manager):

#     def get_process(self):
#         result=self.all()
#         return result

# class ContractoManager(models.Manager):

#     def get_contracs(self):
#         result=self.all()
#         return result

# class UnidadTerritorialoManager(models.Manager):

#     def get_unidades(self):
#         result=self.all()
#         return result

# class MunicipioManager(models.Manager):

#     def get_municipios(self):
#         result=self.all()
#         return result

# class VeredaManager(models.Manager):

#     def get_veredas(self):
#         result=self.all()
#         return result

# class SubestacionManager(models.Manager):

#     def get_subestaciones(self):
#         result=self.all()
#         return result

# class CircuitoManager(models.Manager):

#     def get_circuitos(self):
#         result=self.all()
#         return result



