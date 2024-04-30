# from rest_framework.generics import (
#     ListAPIView, 
#     CreateAPIView, 
#     UpdateAPIView,
#     DestroyAPIView,
#     RetrieveAPIView
#     )

# from .serializers import HoraExtraSerializer,CrearHESerializer
# from rest_framework.views import APIView
# from .models import HoraExtra, CalendarioFestivo
# from ..users_management.models import User


# # from django.db.models import F
# # from django.urls import reverse_lazy
# # from ..models.trazabilidad import Trazabilidad
# from rest_framework.response import Response
# from rest_framework.exceptions import AuthenticationFailed
# import jwt, datetime
# from rest_framework import status

# from rest_framework.response import Response
# # from rest_framework.exceptions import NotFound


# # 1. CREAR HORAS EXTRAS ----------------------------------------
# class CrearHoraExtra(CreateAPIView):
#     serializer_class=CrearHESerializer
#     def post(self, request):
#         token=request.COOKIES.get('jwt')
#         if not token:
#             raise AuthenticationFailed("Unauthenticated!")
#         try:
#             payload=jwt.decode(token,'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed("Unauthenticated!")
        
#         usuario=User.objects.get(username=payload['username'])

#         # Implementando la lógica de los código
#         reporte_he=request.data
#         reporte_he["cod_4185"]=0
#         reporte_he["cod_4215"]=0
#         reporte_he["cod_4225"]=0
#         reporte_he["cod_4230"]=0
#         reporte_he["cod_4235"]=0
#         reporte_he["cod_4240"]=0
#         reporte_he["cod_4245"]=0
#         reporte_he["cod_4270"]=0
#         reporte_he["cod_4275"]=0
#         reporte_he["cod_4280"]=0
#         reporte_he["cod_9050"]=0
#         reporte_he["cod_9054"]=0
        
#         festivo=False
#         fecha=datetime.datetime.strptime(request.data["fecha"], '%Y-%m-%d')
#         h_fin=datetime.datetime.strptime(request.data["hora_salida"],'%H:%M').time()
#         h_inicio=datetime.datetime.strptime(request.data["hora_entrada"],'%H:%M').time()
#         dia=fecha.weekday()
#         q_he=round((datetime.datetime.combine(fecha,h_fin) - datetime.datetime.combine(fecha,h_inicio)).total_seconds()/3600,1)

#         print(q_he)

#         # Validar festivos
#         dias_festivos=CalendarioFestivo.objects.filter(fecha=fecha).first()
#         if dias_festivos:
#             festivo=True

#         print(festivo)

#         # Si son más de 9 horas (8 HE y 1 BONO DE ALIMENTACÍÓN)
#         # Si comeinza antes del medio día.
#         if h_inicio < datetime.datetime.strptime('12:00','%H:%M').time() and q_he > 9:
#             reporte_he["cod_4280"]=1
#             q_he=q_he-1

#         # Domingo
#         if dia==6:
#             if q_he > 8 and h_fin < datetime.datetime.strptime('21:00','%H:%M').time():
#                 reporte_he["cod_4185"]=8
#                 reporte_he["cod_4240"]=round(q_he-8,1)
#             elif q_he > 8 and h_fin > datetime.datetime.strptime('21:00','%H:%M').time():
#                 h_21=datetime.datetime.strptime("21:00",'%H:%M').time()
#                 reporte_he["cod_4245"]=round((datetime.datetime.combine(fecha,h_fin) - datetime.datetime.combine(fecha,h_21)).total_seconds()/3600,1)
#                 q_he=round(q_he-reporte_he["cod_4245"],1)
#                 if q_he > 8:
#                     reporte_he["cod_4185"]=8
#                     reporte_he["cod_4240"]=round(q_he-8,1)
#                 elif q_he < 8:
#                     reporte_he["cod_4185"]=round(q_he,1)
#             elif q_he < 8:
#                 reporte_he["cod_4185"]=round(q_he,1)
        
#         # Si el día es frestivo
#         elif dia!= 6 and festivo:
#             if q_he > 8 and h_fin < datetime.datetime.strptime('21:00','%H:%M').time():
#                 reporte_he["cod_4215"]=8
#                 reporte_he["cod_4270"]=round(q_he-8,1)
#             elif q_he > 8 and h_fin > datetime.datetime.strptime('21:00','%H:%M').time():
#                 h_21=datetime.datetime.strptime("21:00",'%H:%M').time()
#                 reporte_he["cod_4275"]=(datetime.datetime.combine(fecha,h_fin) - datetime.datetime.combine(fecha,h_21)).total_seconds()/3600
#                 q_he=round(q_he-reporte_he["cod_4275"],1)
#                 if q_he > 8:
#                     reporte_he["cod_4215"]=8
#                     reporte_he["cod_4270"]=round(q_he-8,1)
#                 elif q_he < 8:
#                     reporte_he["cod_4215"]=round(q_he,1)
#             elif q_he < 8:
#                 reporte_he["cod_4215"]=round(q_he,1)
        
#         # Si el día es diferente a domingo o festivo
#         elif dia!= 6 and festivo==False:
#             if q_he > 8 and h_fin < datetime.datetime.strptime('21:00','%H:%M').time():
#                 reporte_he["cod_4230"]=round(q_he,1)
#             elif q_he > 8 and h_fin > datetime.datetime.strptime('21:00','%H:%M').time():
#                 h_21=datetime.datetime.strptime("21:00",'%H:%M').time()
#                 reporte_he["cod_4235"]=(datetime.datetime.combine(fecha,h_fin) - datetime.datetime.combine(fecha,h_21)).total_seconds()/3600
#                 reporte_he["cod_4230"]=round(q_he-reporte_he["cod_4235"],1)
#             elif q_he < 8:
#                 reporte_he["cod_4230"]=round(q_he,1)

#         response=HoraExtra.objects.registrar_hora_extra(reporte_he,usuario)
#         return response
# # ---------------------------------------------------------------------


# # 2. LISTAR HORAS EXTRAS DE UN USUARIO --------------------------------
# class ListarHorasExtras(ListAPIView):
#     serializer_class=HoraExtraSerializer
#     def get_queryset(self):
#         token=self.request.COOKIES.get('jwt')
#         if not token:
#             raise AuthenticationFailed("Unauthenticated!")
#         try:
#             payload=jwt.decode(token,'secret',algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed("Unauthenticated!")
        
#         usuario=User.objects.get(username=payload['username'])
        
#         queryset=HoraExtra.objects.obtener_horas_extras(usuario)
#         return queryset
# # ---------------------------------------------------------------------

# # 3. OBTENER DETALLES DE UNA HORA EXTRA-------------- ---------------
# class ObtenerHoraExtra(RetrieveAPIView):
#     serializer_class = HoraExtraSerializer

#     def get_queryset(self):
#         token = self.request.COOKIES.get('jwt')
#         if not token:
#             raise AuthenticationFailed("Unauthenticated!")

#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed("Unauthenticated!")

#         # Obtiene el parámetro de la URL 'pk' para buscar el trabajo específico
#         pk = self.kwargs.get('pk')
#         queryset = HoraExtra.objects.filter(id_hora_extra=pk)
#         return queryset
# # ---------------------------------------------------------------------

# # 4. ACTUALIZAR HORA EXTRA ----------------------------
# class ActualizarHoraExtra(UpdateAPIView):
#     def put(self, request, pk):
#         token=request.COOKIES.get('jwt')
#         if not token:
#             raise AuthenticationFailed("Unauthenticated!")
#         try:
#             payload=jwt.decode(token,'secret',algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed("Unauthenticated!")

#         # usuario=User.objects.get(username=payload['username'])
#         pk = self.kwargs.get('pk')

#         try:
#             response=HoraExtra.objects.actualizar_horas_extras(request.data, pk)
#             return Response({'message': f"La {response} fue actualizada"}, status=201)
#         except Exception as e:
#             mensaje = str(e)
#             status_code = e.status_code
#             return Response({'error': mensaje}, status=401)
# # ---------------------------------------------------------------------


# # 5. ELIMINAR HORA EXTRA ----------------------------------------------
# class EliminarHoraExtra(DestroyAPIView):
#     def post(self, request):
#         token=request.COOKIES.get('jwt')
#         if not token:
#             raise AuthenticationFailed("Unauthenticated!")
#         try:
#             payload=jwt.decode(token,'secret',algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed("Unauthenticated!")
#     queryset=HoraExtra.objects.all()
#     serializer_class=HoraExtraSerializer
#     lookup_field='pk'
# # ---------------------------------------------------------------------