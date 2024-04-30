from django.db import models


class ProcessManager(models.Manager):

    def get_process(self):
        result = self.all()
        return result

