from . import views
from django.urls import path

urlpatterns = [
   #path('afiliadoLista', views.afiliadoLista, name='afiliadoLista'), 
   path('crearFederacion',views.crearFederacion, name='crearFederacion'),
   path('listarFedeacion',views.listarFedeacion, name='listarFedeacion'),
 
]
