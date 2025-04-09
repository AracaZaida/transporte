from . import views
from django.urls import path

urlpatterns = [
   #path('afiliadoLista', views.afiliadoLista, name='afiliadoLista'), 
   path('crearTramite',views.crearTramite, name='crearTramite'),
   path('listarTramite',views.listarTramite, name='listarTramite'),
   path('crearTipo_tramite', views.crearTipo_tramite, name='crearTipo_tramite'),
   path('tramite/datalle/<int:id>', views.detalleTramite, name='detalleTramite'),

   path('tramite/aprobar/<int:id>', views.aprobarTramite, name='aprobarTramite'),
    
   path('tramite/anular/<int:id>', views.anularTramite, name='anularTramite')
 
]
