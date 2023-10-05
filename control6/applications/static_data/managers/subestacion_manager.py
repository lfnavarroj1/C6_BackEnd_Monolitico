from django.db import models


class SubestacionManager(models.Manager):
    def get_subestaciones(self):
        result=self.all()
        return result




