from rest_framework.generics import (
    ListAPIView, 
    CreateAPIView, 
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView
    )
from rest_framework.views import APIView
from ..models.trabajo import Trabajo
from ..models.trazabilidad import Trazabilidad
from ...users.models import User
from ..serializers.trabajo_serializer import TrabajoSerializer, CrearTrabajoSerializer

# from django.db.models import F
# from django.urls import reverse_lazy
# from ..models.trazabilidad import Trazabilidad
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt,json #, datetime
from rest_framework import status

from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from ...static_data.models.ruta_proceso import RutaProceso

from ..errores import CampoRequeridoError, NoTienSiguienteEstado

