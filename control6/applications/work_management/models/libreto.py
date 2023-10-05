# from django.db import models
# from ...static_data.models import (Process,EstructuraPresupuestal,
#                                      Municipio,Vereda,Subestacion,
#                                      Circuito,EstadoTrabajo, TipoNodo,
#                                      TipoTrabajo,TipoInstalacion, 
#                                      NivelTension, NormaCodensa, TipoItem,Prestacion,
#                                      Material
# )

# from ...users.models import User

# # Import managers
# from ..managers.managers import TrabajoManager

# # Create your models here.


# class Libreto(models.Model):
#     ESTADO_LIBRETO=(
#         ('0','CARGADO'),
#         ('1','LIBERADO TECNICAMENTE'),
#         ('2','LIBERADO CONTABLEMENTE'),
#         ('3','CON CONFORMIDAD ENTREGADA'),
#     )
#     trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE)
#     lcl = models.ForeignKey(Lcl, on_delete=models.CASCADE)
#     numero_libreto = models.CharField(max_length=3)
#     valor_mod = models.FloatField()
#     valor_mat = models.FloatField()
#     estado_libreto = models.CharField(max_length=1, choices=ESTADO_LIBRETO)

#     def __str__(self) -> str:
#         return str(self.numero_libreto)