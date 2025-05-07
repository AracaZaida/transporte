from . import views
from django.urls import path

urlpatterns = [
   #path('afiliadoLista', views.afiliadoLista, name='afiliadoLista'), 
   path('crearUsuario',views.crearUsuario, name='crearUsuario'),
   path('listarUsuario',views.listarUsuario, name='listarUsuario'),
     path('',views.login_sistema, name='login'),
       path('home',views.home, name='home'),
       path('editar_user/<int:usuario_id>',views.editar_user, name='editar_user'),
        path('elimar_usario/<int:usuario_id>', views.elimar_usario, name='elimar_usario'),
 
]
