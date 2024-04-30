# from rest_framework.views import APIView
# from ..users_management.views import ValidateUser
# from rest_framework.response import Response
# from models import *
# from serializers import *


# class ListarUnidadTerritorial(APIView):
#     def get(self, request):
#             user = ValidateUser(request)

#             if user["valid_user"]:      
#                 response = UnidadTerritorial.objects.all()
#                 serializer = UnidadTerritorialSerializer(response, many=True)
#                 return Response(serializer.data)
            
#             return Response(user)
    
# class ListarMunicipio(APIView):

#         def get(self, request):
#             user = ValidateUser(request)

#             if user["valid_user"]:

#                 numero_ut=self.kwargs.get('pk')
#                 municipios=Municipio.objects.filter(unidad_territorial__numero=numero_ut)
#                 return municipios

#                 vp1 = self.request.query_params.get('vp', '')
#                 ve1 = self.request.query_params.get('ve', '')
#                 kword = self.request.query_params.get('kw', '')
#                 vect_procesos = vp1.split(',')
#                 vect_estados  = ve1.split(',')
            
#                 response = Trabajo.objects.filtrar_trabajos(vect_procesos, vect_estados, kword, user["user"])
#                 serializer = TrabajoSerializer(response, many=True)

#                 return Response(serializer.data)
            
#             return Response(user)
        

#     serializer_class=MunicipioSerializer
#     def get_queryset(self):
#         numero_ut=self.kwargs.get('pk')
#         municipios=Municipio.objects.filter(unidad_territorial__numero=numero_ut)
#         return municipios
    
# class ListarVereda(APIView):

#         def get(self, request):
#             user = ValidateUser(request)

#             if user["valid_user"]:
#                 vp1 = self.request.query_params.get('vp', '')
#                 ve1 = self.request.query_params.get('ve', '')
#                 kword = self.request.query_params.get('kw', '')
#                 vect_procesos = vp1.split(',')
#                 vect_estados  = ve1.split(',')
            
#                 response = Trabajo.objects.filtrar_trabajos(vect_procesos, vect_estados, kword, user["user"])
#                 serializer = TrabajoSerializer(response, many=True)

#                 return Response(serializer.data)
            
#             return Response(user)
        
#         municipio_pk=self.kwargs.get('pk')
#         veredas=Vereda.objects.filter(municipio_id=municipio_pk)
#         return veredas