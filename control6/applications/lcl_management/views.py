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
from ..users.views import ValidateUser


class AgregarLclView(CreateAPIView):
    serializer_class = LclSerializer
    def post(self, request):
        usuario = ValidateUser(request)
        
        if usuario:
            return  Lcl.objects.agregar_lcl(request.data, usuario)
        return usuario


class ListarLclView(ListAPIView):
    serializer_class = LclListaSerializer
    def get_queryset(self):
        usuario = ValidateUser(self.request)
        
        if usuario:
            vp1=self.request.query_params.get('vp','')
            ve1=self.request.query_params.get('ve','')
            kword=self.request.query_params.get('kw','')
            vect_procesos=vp1.split(',')
            vect_estados=ve1.split(',')

            # Indicar unidad territorial y contrato.

            response=Lcl.objects.filtrar_lcl(vect_procesos,vect_estados,kword)
            return response
        
        return usuario
    

class ListarLclTrabajoView(ListAPIView):
    serializer_class = LclSerializer
    def get_queryset(self):
        usuario = ValidateUser(self.request)

        if usuario:
            pk = self.kwargs.get('pk')
            queryset = Lcl.objects.obtener_lcls(pk)
            return queryset
        
        return usuario


class ObtenerDetalleLclView(RetrieveAPIView):
    serializer_class = LclSerializer

    def get_queryset(self):
        usuario = ValidateUser(self.request)

        if usuario:
            pk = self.kwargs.get('pk')
            queryset = Lcl.objects.filter(lcl=pk)
            return queryset
        
        return usuario


class ActualizarLclView(UpdateAPIView):
    def put(self, request, pk):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        # usuario=User.objects.get(username=payload['username'])
        pk = self.kwargs.get('pk')

        try:
            response=Lcl.objects.actualizar_lcl(request.data, pk)
            # dic=request.data
            # campos_actualizados=""
            # for campo in dic.keys():
            #     campos_actualizados=campos_actualizados +", "+campo
            
            # datos={}
            # datos["trabajo"]=response.id_control
            # datos["comentario_trazabilidad"]=f"Se actualizaron los campos {campos_actualizados} del trabajo {response.id_control}"
            # Odm.objects.registrar_trazabilidad(datos, usuario)
            return Response({'message': f"La {response} fue actualizada"}, status=201)
        except Exception as e:
            mensaje = str(e)
            status_code = 400
            return Response({'error': mensaje}, status=400)


class EliminarLclView(DestroyAPIView):
    def post(self, request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
    queryset=Lcl.objects.all()
    serializer_class=LclSerializer
    lookup_field='pk'


class ContarLclPorProcesosView(APIView):
    # serializer_class=ProcesoSerializer
    def get(self,request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        vp1=self.request.query_params.get('vp','')
        ve1=self.request.query_params.get('ve','')
        kword=self.request.query_params.get('kw','')
        vect_procesos=vp1.split(',')
        vect_estados=ve1.split(',')
        
        response=Lcl.objects.filtrar_lcl(vect_procesos,vect_estados,kword)
        serializer=LclListaSerializer(response,many=True)
        procesos=[item for proceso in serializer.data for item in list(proceso['proceso'])]
        conteo_nombre_procesos=Counter(procesos)
        return Response(conteo_nombre_procesos, status=200)


class ContarLclPorEstadoView(APIView):
    # serializer_class=ProcesoSerializer
    def get(self,request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        try:
            payload=jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")
        
        vp1=self.request.query_params.get('vp','')
        ve1=self.request.query_params.get('ve','')
        kword=self.request.query_params.get('kw','')
        vect_procesos=vp1.split(',')
        vect_estados=ve1.split(',')
        
        response=Lcl.objects.filtrar_lcl(vect_procesos,vect_estados,kword)
        serializer=LclListaSerializer(response,many=True)
        estado=[item['estado_lcl'] for item in serializer.data]
        conteo_estado_lcl=Counter(estado)
        return Response(conteo_estado_lcl, status=200)
