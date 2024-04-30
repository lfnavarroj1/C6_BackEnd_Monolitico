from rest_framework.views import APIView
from .models import ResultBt
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt

class ActualizarDatosBoardView(APIView):
    def post(self, request):

        usuario = ValidateUser(request)

        if usuario["valid_user"]:
        
            vector_uno = self.request.query_params.get('vector_unidades_territoriales' , '')
            vector_dos = self.request.query_params.get('vector_contratos' , '')
            vector_tres = self.request.query_params.get('vector_estados' , '')
            vector_cuatro = self.request.query_params.get('vector_anio' , '')
            vector_cinco = self.request.query_params.get('vector_mes' , '')
            vector_seis = self.request.query_params.get('vector_estados_inspecciones' , '')

            
            vector_unidades_territoriales = vector_uno.split(',')
            vector_contratos = vector_dos.split(',')
            vector_estados = vector_tres.split(',')
            vector_anio = vector_cuatro.split(',')
            vector_meses = vector_cinco.split(',')
            vector_estados_inspecciones = vector_seis.split( ',' )
            kword = self.request.query_params.get('kw' , '')
            
            if usuario["user"].lider_hse:
                response = ManiobrasTqi.objects.filtrar_maniobras( vector_unidades_territoriales, vector_contratos, vector_estados, vector_anio, vector_meses, kword )

            
            else:
                response = ManiobrasTqi.objects.filter(
                                                        anio__in = vector_anio, 
                                                        mes__in = vector_meses,
                                                        inspector_asingado = usuario['user'],
                                                        codigo__icontains = kword,
                                                    ).all()
            
            serializer = ManiobrasTqiSerializer(response, many=True)
                
            return Response(serializer.data)
        
        return Response(usuario)

