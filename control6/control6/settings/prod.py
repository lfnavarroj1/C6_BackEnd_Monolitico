from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "db_backend_c6",
        "USER": "postgres",
        "PASSWORD": "nativa1234",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# STATIC_URL = '/static/'
# STATIC_ROOT=BASE_DIR/'staticfiles/'
# STATICFILES_DIRS=[BASE_DIR/'static']

# MEDIA_URL='/media/'
# MEDIA_ROOT=BASE_DIR/'media/'


# CONFIGURACIÓN DEL BUKETS PARA LA CARGA DE ARCHIVOS

AWS_ACCESS_KEY_ID = 'TU_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'TU_SECRET_ACCESS_KEY'
AWS_STORAGE_BUCKET_NAME = 'NOMBRE_DE_TU_SPACE'
AWS_S3_ENDPOINT_URL = 'https://nyc3.digitaloceanspaces.com'  # URL de tu Space
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.nyc3.digitaloceanspaces.com'
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# Configuración adicional de almacenamiento estático
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Configuración adicional de archivos multimedia si es necesario
# MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'