from . import views
from django.urls import path

urlpatterns = [
   path('', views.afiliadoLista, name='afiliadoLista'), 
   path('crearAfiliados',views.crearAfiliados, name='crearAfiliados') 
 
]

