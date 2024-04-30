from django.db import models

from django.db.models import Q

class UsuarioManager(models.Manager):  
    def filtrar_usuarios(self, vector_unidades_territoriales, vector_contratos, kword):
        result = self.filter(
            Q(unidades_territoriales__in = vector_unidades_territoriales),
            Q(contratos__in = vector_contratos), 
            Q(username__icontains = kword ) | Q( assigned__icontains = kword ) | Q( first_name__icontains = kword ) | Q( last_name__icontains = kword ),
        )
        return result