from rest_framework.generics import (
    ListAPIView, 
    CreateAPIView, 
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView
    )

from rest_framework.views import APIView

from .models import Odm
from .serializers import OdmSerializer
from ..users_management.models import User
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from ..users_management.views import ValidateUser




class CrearOdm(APIView):
    def post(self, request):
        
        usuario = ValidateUser(request)

        if usuario["valid_user"]:
        
            response = Odm.objects.agregar_odm(request.data)
            return response
        
        return Response(usuario)



# 2. LISTAR ODM ASOCIADAS A UN TRABAJO --------------------------
class ListarOdm(APIView):
    def get(self, request, *args,**kwargs):

        usuario = ValidateUser(request)

        if usuario['valid_user']:

            pk = self.kwargs.get('pk')

            queryset=Odm.objects.obtener_odms(pk)
            response = Odm.objects.obtener_odms(request.data)
            return queryset, response
        return Response(usuario)
# ---------------------------------------------------------------------


# 3. OBTENER DETALLES DE UNA ODM ASOCIADAS A UN TRABAJO ---------------
class ObtenerOdm(APIView):
        def get(self, request, *args,**kwargs):

            usuario = ValidateUser(request)
            if usuario['valid_user']:

                pk = self.kwargs.get('pk')
                queryset = Odm.objects.filter(odm=pk)
                response = Odm.objects.filter(request.data)
                return queryset, response
            return Response(usuario)
# ---------------------------------------------------------------------


# 4. ACTUALIZAR ODM ASOCIADAS A UN TRABAJO ----------------------------
class ActualizarOdm(APIView):
        def put(self, request, pk):
            usuario = ValidateUser(request)
            if usuario['valid_user']:
                pk = self.kwargs.get('pk')
                response=Odm.objects.actualizar_odm(request.data, pk)
                return response
            return Response(usuario)
# ---------------------------------------------------------------------


# 5. ELIMINAR ODM ASOCIADAS A UN TRABAJO ------------------------------
class EliminarOdm(APIView):
    def post(self, request, *args,**kwargs):
        usuario = ValidateUser(request)
        if usuario['valid_user']:
            pk = self.kwargs.get('pk')
            queryset=Odm.objects.all(request.data, pk)
            return queryset
        return Response(usuario)
# ---------------------------------------------------------------------

