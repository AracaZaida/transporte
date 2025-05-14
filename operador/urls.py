from . import views
from django.urls import path

urlpatterns = [
   #path('afiliadoLista', views.afiliadoLista, name='afiliadoLista'), 
   path('crearOperdor',views.crearOperdor, name='crearOperdor'),
   path('listarOperador',views.listarOperador, name='listarOperador'),
   path('editar_operador/<int:ope_id>/', views.editar_operador, name='editar_operador'),
   path('eliminar_operador/<int:ope_id>/', views.eliminar_operador, name='eliminar_operador'),
 
]
