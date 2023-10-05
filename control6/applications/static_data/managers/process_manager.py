from django.db import models
# from django.db.models import Q,Count


class ProcesoManager(models.Manager):
    def get_process(self):
        result=self.all()
        return result