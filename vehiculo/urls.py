from . import views
from django.urls import path

urlpatterns = [
   path('crearVehiculo', views.crearVehiculo, name='crearVehiculo'), 
   path('listaVehiculo',views.listaVehiculo, name='listaVehiculo')
   
 
]