from rest_framework.generics import (
    ListAPIView, 
    CreateAPIView, 
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView
    )
from rest_framework.views import APIView
from .models import Lcl
from .serializers import LclSerializer, LclListaSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt 
from rest_framework.response import Response
from collections import Counter
from ..users_management.views import ValidateUser


class AgregarLclView(APIView):
    def post(self, request):
        usuario = ValidateUser(request)
        if usuario['valid_user']:
            response = Lcl.objects.agregar_lcl(request.data)
            return response
        return Response(usuario)


class ListarLclView(APIView):
    def get(self, request):
        usuario = ValidateUser(request)
        
        if usuario['valid_user']:
            vp1=self.request.query_params.get('vp','')
            ve1=self.request.query_params.get('ve','')
            kword=self.request.query_params.get('kw','')
            vect_procesos=vp1.split(',')
            vect_estados=ve1.split(',')

            response=Lcl.objects.filtrar_lcl(request.data)
            return response
        
        return Response(usuario)
    

class ListarLclTrabajoView(APIView):
    def get(self, request, *args,**kwargs):
        usuario = ValidateUser(request)

        if usuario['valid_user']:
            pk = self.kwargs.get('pk')
            queryset = Lcl.objects.obtener_lcls(request.data ,pk)
            return queryset
        
        return Response(usuario)


class ObtenerDetalleLclView(APIView):

    def get(self, request, *args,**kwargs):
        usuario = ValidateUser(request)

        if usuario['valid_user']:
            pk = self.kwargs.get('pk')
            queryset = Lcl.objects.filter(request.data , pk)
            return queryset
        
        return Response(usuario)


class ActualizarLclView(APIView):
    def put(self, request, pk):
        usuario = ValidateUser(request)
        if usuario['valid_user']:
            pk = self.kwargs.get('pk')
            queryset = Lcl.objects.actualizar_lcl(request.data, pk)
            return queryset

        return Response(usuario)


class EliminarLclView(APIView):
    def post(self, request):
        usuario = ValidateUser(request)
        if usuario['valid_user']:
            pk = self.kwargs.get('pk')
            queryset=Lcl.objects.all(request.data, pk)
            return queryset
        
        return Response(usuario)



class ContarLclPorProcesosView(APIView):
    def get(self,request):
        usuario = ValidateUser(request)
        if usuario['valid_user']:
            vp1=self.request.query_params.get('vp','')
            ve1=self.request.query_params.get('ve','')
            kword=self.request.query_params.get('kw','')
            vect_procesos=vp1.split(',')
            vect_estados=ve1.split(',')
        
            response=Lcl.objects.filtrar_lcl(request.data ,vect_procesos,vect_estados,kword)
            return response
        return Response(usuario)


class ContarLclPorEstadoView(APIView):
    def get(self,request):
        usuario = ValidateUser(request)
        if usuario['valid_user']:
        
            vp1=self.request.query_params.get('vp','')
            ve1=self.request.query_params.get('ve','')
            kword=self.request.query_params.get('kw','')
            vect_procesos=vp1.split(',')
            vect_estados=ve1.split(',')
            
            response=Lcl.objects.filtrar_lcl(request.data ,vect_procesos,vect_estados,kword)
            return response
        return Response(usuario)
