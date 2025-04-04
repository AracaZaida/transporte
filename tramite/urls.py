from . import views
from django.urls import path

urlpatterns = [
   #path('afiliadoLista', views.afiliadoLista, name='afiliadoLista'), 
   path('crearTramite',views.crearTramite, name='crearTramite'),
   path('listarTramite',views.listarTramite, name='listarTramite'),
 
]
