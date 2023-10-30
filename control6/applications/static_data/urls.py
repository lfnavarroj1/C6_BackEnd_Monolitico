from django.urls import path
from .views import views

urlpatterns = [
    path('get-process/', views.ListarProceso.as_view(), name="get-process" ),
    path('get-contracts/', views.ListarContrato.as_view(), name="get-contracts" ),
    path('get-unit/', views.ListarUnidadTerritorial.as_view(), name="get-unit" ),
    path('get-mun/<pk>', views.ListarMunicipio.as_view(), name="get-mun" ),
    path('get-verdas/<pk>', views.ListarVereda.as_view(), name="get-veredas" ),
    path('get-subtaciones/', views.ListarSubestacion.as_view(), name="get-subtaciones" ),
    path('get-circuitos/<pk>', views.ListarCircuito.as_view(), name="get-circuitos" ),
]
