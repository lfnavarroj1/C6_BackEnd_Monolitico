import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'control6.settings')


app = Celery("control6")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()