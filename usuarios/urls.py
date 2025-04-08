from . import views
from django.urls import path

urlpatterns = [
   #path('afiliadoLista', views.afiliadoLista, name='afiliadoLista'), 
   path('crearUsuario',views.crearUsuario, name='crearUsuario'),
   path('listarUsuario',views.listarUsuario, name='listarUsuario'),
 
]
