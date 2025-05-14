from . import views
from django.urls import path

urlpatterns = [
   #path('afiliadoLista', views.afiliadoLista, name='afiliadoLista'), 
   path('crearFederacion',views.crearFederacion, name='crearFederacion'),
   path('listarFedeacion',views.listarFedeacion, name='listarFedeacion'),
   path('editar_federacion/<int:fer_id>/', views.editar_federacion, name='editar_federacion'),
   path('eliminar_federacion/<int:fer_id>/', views.eliminar_federacion, name='eliminar_federacion'),
 
]
