# # import datetime
# # from django.forms.models import BaseModelForm
# # from django.http import HttpResponse
# # from django.shortcuts import render
# from rest_framework.generics import ListAPIView, CreateAPIView
# # from rest_framework.views import APIView
# # from django.contrib.auth.mixins import LoginRequiredMixin
# # from ..models.programacion import Trabajo, Trazabilidad
# from ..models.trabajo import Trabajo
# from ..models.trazabilidad import Trazabilidad
# from ..serializers.trabajo_serializers import TrabajoSerializer, CreateWorkSerializer
# from django.db.models import F
# # from django.urls import reverse_lazy
# from rest_framework.response import Response
# from rest_framework.exceptions import AuthenticationFailed
# import jwt #, datetime
# from rest_framework import status





# # Import forms
# # from .forms import TrabajoForms, ValorizacionReplanteoForms, ValorizacionRevisada


# # 1. LISTAR TRABAJOS ----------------------------------------

# class ListarTrabajos(ListAPIView):
#     serializer_class=TrabajoSerializer

#     # template_name='gestion_trabajos/lista.html'
#     # context_object_name='trabajos'
#     # login_url=reverse_lazy('users_app:login-usuario')
    

#     def get_queryset(self):
#         # palabra_clave=self.request.GET.get('kword','')
#         # usuario=self.request.user

#         # Procesos usuarios
#         # procesos =list(Trabajo.objects.lista_procesos_usuario(usuario))

#         # Estados por usuaarios
#         # estados=list(Trabajo.objects.lista_estado_usuario(usuario))

#         # Conteo Estados

#         # procesos_filtro=[]
#         # estados_filtro=[]

#         # # Optimizar seralizando bien el Trabajo

#         # for p in procesos:
#         #     if self.request.GET.get(str(p)):
#         #         procesos_filtro.append(p)
        
#         # for e in estados:
#         #     if self.request.GET.get(str(e)):
#         #         estados_filtro.append(e)

#         trabajos=Trabajo.objects.lista_trabajos()
#         return trabajos
    
#     # def get_context_data(self, **kwargs):
#     #     context = super(ListarTrabajos,self).get_context_data(**kwargs)
#     #     context['form']=TrabajoForms
#     #     return context

# # ---------------------------------------------------------------------

# # 2. CREAR UN NUEVO TRABAJO ------------------------------------------------

# class TrabajoCreateView(CreateAPIView):
#     serializer_class=CreateWorkSerializer
#     def post(self, request):
#         token=request.COOKIES.get('jwt')
#         if not token:
#             raise AuthenticationFailed("Unauthenticated!")
#         try:
#             payload=jwt.decode(token,'secret',algorithms=['HS256'])
            

#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed("Unauthenticated!")
        
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

# # # ---------------------------------------------------------------------
# # 3. ACTUALIZAR UN TRABAJO

# class TrabajoUpdateView(LoginRequiredMixin,UpdateView):
#     model = Trabajo
#     template_name = "gestion_trabajos/detalle_trabajo.html"
#     login_url=reverse_lazy('users_app:login-usuario')
#     fields=[
#         'pms_quotation',
#         'pms_need',
#         'proceso',
#         'caso_radicado',
#         'direccion',
#         'alcance',
#         'priorizacion',
#         'estructura_presupuestal',
#         'municipio',
#         'vereda',
#         'subestacion',
#         'circuito',
#         'estado_trabajo',
#     ]

#     def get_context_data(self, **kwargs):
#         context = super(TrabajoUpdateView,self).get_context_data(**kwargs)
#         context["trazabilidad"] = Trazabilidad.objects.filter(
#             trabajo=context['trabajo'].id,
#         )
#         context["val_replanteo"] = ValorizacionReplanteoForms
#         context["val_revisada"] = ValorizacionRevisada
#         return context
    
# # ---------------------------------------------------------------------

# 4. ELIMINAR UN TRABAJO



# # Creación de un trabajo

# class TrazabilidadCreateView(CreateView):
#     model=Trazabilidad
#     template_name = "gestion_trabajos/detalle_trabajo.html"
#     success_url = reverse_lazy('gestiontrabajos:actualizar-trabajo')


# # Crear Valorización

# class ValorizacionCreateView(CreateView):
#     model = Valorizacion
#     template_name = "gestion_trabajos/detalle_trabajo.html"
#     success_url = reverse_lazy('gestiontrabajos:actualizar-trabajo')

#     def get_context_data(self, **kwargs):
#         context = super(ValorizacionCreateView,self).get_context_data(**kwargs)
#         context["valorización"] = ValorizacionForms 
#         return context
    
# 5. PASAR EL SIGUIETE ESTADO DE UN TRABAJO


# 6 DEVOLVER ESTADO DE UN TRABAJO



