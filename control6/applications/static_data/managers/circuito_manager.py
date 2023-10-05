from django.db import models


class CircuitoManager(models.Manager):
    def get_circuitos(self):
        result=self.all()
        return result



