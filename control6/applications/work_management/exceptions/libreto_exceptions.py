from rest_framework.exceptions import APIException

class LibretoNoEncontrado(APIException):
    status_code = 404
    default_detail = 'Libreto no encontrado.'

class CustomServerErrorException(APIException):
    status_code = 500
    default_detail = 'Error interno del servidor.'