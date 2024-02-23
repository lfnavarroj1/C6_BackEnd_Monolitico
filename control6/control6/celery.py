from celery import Celery
from celery.schedules import crontab

app = Celery("control6")
app.config_from_object('django.conf:settings.base', namespace='CELERY')
app.autodiscover_tasks()


# Configuración de tareas periódicas
app.conf.beat_schedule = {
    'mi-tarea-programada': {
        'task': 'control6.actualizar_maniobras.actualizar_maniobras',  # Ruta a tu tarea
        'schedule': crontab(minute='*/10'),  # Cada 10 minutos
    },
}