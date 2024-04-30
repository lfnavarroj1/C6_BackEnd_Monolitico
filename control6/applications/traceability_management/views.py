from rest_framework.generics import (
        ListAPIView, 
        CreateAPIView, 
    )
from .models import TrazabilidadTrabajo, TrazabilidadInspeccionesTqi
from .serializers import TrazabilidadTrabajoSerializer, TrazabilidadInspeccionesTqiSerializer
from ..users_management.views import ValidateUser


class CrearTrazabilidadTrabajo(CreateAPIView):
    serializer_class = TrazabilidadTrabajoSerializer
    def post(self, request):        
        usuario=ValidateUser(request)
        if usuario:
            response=TrazabilidadTrabajo.objects.registrar_trazabilidad(request.data, usuario)
            return response
        return usuario

class ListarTrazabilidadTrabajo(ListAPIView):
    serializer_class = TrazabilidadTrabajoSerializer
    def get_queryset(self):
        usuario=ValidateUser(self.request)
        if usuario:
            pk = self.kwargs.get('pk')
            queryset = TrazabilidadTrabajo.objects.obtener_trazabilidad(pk)
        return queryset


class CrearTrazabilidadInspeccionesTqi(CreateAPIView):
    serializer_class = TrazabilidadInspeccionesTqiSerializer
    def post(self, request):        
        usuario=ValidateUser(request)
        if usuario:
            response=TrazabilidadInspeccionesTqi.objects.registrar_trazabilidad(request.data, usuario)
            return response
        return usuario

class ListarTrazabilidadInspeccionesTqi(ListAPIView):
    serializer_class = TrazabilidadInspeccionesTqiSerializer
    def get_queryset(self):
        usuario=ValidateUser(self.request)
        if usuario:
            pk = self.kwargs.get('pk')
            queryset = TrazabilidadInspeccionesTqi.objects.obtener_trazabilidad(pk)
        return queryset