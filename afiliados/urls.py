from . import views
from django.urls import path

urlpatterns = [
   path('afiliadoLista', views.afiliadoLista, name='afiliadoLista'), 
   path('crearAfiliados',views.crearAfiliados, name='crearAfiliados'),
   path('editar_afiliado/<int:afi_id>/', views.editar_afiliado, name='editar_afiliado'),
   path('eliminar_afiliado<int:afi_id>/', views.eliminar_afiliado, name='eliminar_afiliado'),

 
]

