from . import views
from django.urls import path

urlpatterns = [
   #path('afiliadoLista', views.afiliadoLista, name='afiliadoLista'), 
   path('crearOperdor',views.crearOperdor, name='crearOperdor'),
   path('listarOperador',views.listarOperador, name='listarOperador'),
 
]
