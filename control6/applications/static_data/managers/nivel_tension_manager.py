from django.db import models
#
class NivelTensionManager(models.Manager):
    def get_nivel_tesnion(self):
        result=self.all()
        return result

