from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name="register" ),
    path('login/', views.LoginUser.as_view(), name="login" ),
    path('get/', views.GetUser.as_view(), name="get_user" ),
    path('logout/', views.LogoutUser.as_view(), name="logout" ),
    
]

