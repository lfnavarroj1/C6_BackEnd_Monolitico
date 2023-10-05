from rest_framework.generics import ListAPIView #,CreateView,DetailView,UpdateView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt #, datetime
from rest_framework import status
# Import Models
from ..models.proceso import Proceso
from ..models.contrato import Contrato
from ..models.unidad_territorial import UnidadTerritorial
from ..models.municipio import Municipio
from ..models.vereda import Vereda
from ..models.subestacion import Subestacion 
from ..models.circuito import Circuito


from ..serializers.serializers import ( 
    ProcesoSerializer, 
    ContratoSerializer, 
    UnidadTerritorialSerializer,
    MunicipioSerializer,
    VeredaSerializer,
    SubestacionSerializer,
    CircuitoSerializer
)
# ------------------------------------------

class ListarProceso(ListAPIView):
    serializer_class=ProcesoSerializer
    def get_queryset(self):
        token=self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        procesos=Proceso.objects.get_process()
        return procesos


class ListarContrato(ListAPIView):
    serializer_class=ContratoSerializer
    def get_queryset(self):
        contratos=Contrato.objects.all()
        return contratos
    
class ListarUnidadTerritorial(ListAPIView):
    serializer_class=UnidadTerritorialSerializer
    def get_queryset(self):
        unidades=UnidadTerritorial.objects.all()
        return unidades
    
class ListarMunicipio(ListAPIView):
    serializer_class=MunicipioSerializer
    def get_queryset(self):
        trabajos=Municipio.objects.all()
        return trabajos
    
class ListarVereda(ListAPIView):
    serializer_class=VeredaSerializer
    def get_queryset(self):
        token=self.request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        trabajos=Vereda.objects.all()
        return trabajos
    
class ListarSubestacion(ListAPIView):
    serializer_class=SubestacionSerializer
    def get_queryset(self):
        trabajos=Subestacion.objects.all()
        return trabajos
    
class ListarCircuito(ListAPIView):
    serializer_class=CircuitoSerializer
    def get_queryset(self):
        trabajos=Circuito.objects.all()
        return trabajos