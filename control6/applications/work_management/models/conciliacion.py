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

    
# class Conciliacion(models.Model):
#     ESTADO_CONCILIACION=(
#         ('0','ENVIADO A ENEL'),
#         ('1','PLANILLAS FIRMADAS'),
#         ('2','SOPORTES CARGADOS'),
#     )
#     trabajo = models.ForeignKey(Trabajo, on_delete=models.CASCADE)
#     lcl = models.ForeignKey(Lcl, on_delete=models.CASCADE)
#     valor_mod = models.FloatField()
#     valor_mat = models.FloatField()
#     estado_conciliacion=models.CharField(max_length=1,choices=ESTADO_CONCILIACION)
#     planillas=models.FileField(upload_to='conciliacion',blank=True, null=True)
#     planilla_firmada=models.FileField(upload_to='planilla_firmada',blank=True, null=True)


#     def __str__(self) -> str:
#         return str(self.trabajo)
    
