from rest_framework.views import APIView
from collections import Counter
from rest_framework.response import Response
import pandas as pd
from .models import Customer


# Create your views here.

class CargarArchivosClientesView(APIView):
    def post(self, request):
        # Ruta al archivo CSV

        # archivo_csv = 'D:/proyectos/control_seis/Cargue de clientes/fragmento_3.csv'
        data_json = request.data
        archivo_csv = data_json["archivo"]
        print(archivo_csv)

        # Leer el archivo CSV utilizando pandas
        df = pd.read_csv(archivo_csv)

        # # Convertir el DataFrame de pandas a una lista de instancias de TuModelo

        instancias = []
        for index, row in df.iterrows():
            instancia = Customer(
                customer_number = row['customer_number'],
                transformer = row['transformer'],
                address = row['address'],
            )
            instancias.append(instancia)

        # Utilizar bulk_create para insertar los registros en la base de datos
        Customer.objects.bulk_create(instancias)

        return Response({'Cargue': "Realizado"}, status=201)