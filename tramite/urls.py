from . import views
from django.urls import path

urlpatterns = [
   #path('afiliadoLista', views.afiliadoLista, name='afiliadoLista'), 
   path('crearTramite',views.crearTramite, name='crearTramite'),
   path('listarTramite',views.listarTramite, name='listarTramite'),

   path('tramite/datalle/<int:id>', views.detalleTramite, name='detalleTramite'),

   path('tramite/aprobar/<int:id>', views.aprobarTramite, name='aprobarTramite'),
    
   path('tramite/anular/<int:id>', views.anularTramite, name='anularTramite'),
      path('tramite/editar/<int:id>', views.editarTramite, name='editarTramite'),
    path('tramite/ver/<int:id>', views.verTramite, name='verTramite'),
    path('verificadoTramite', views.verificadoTramite, name='verificadoTramite'),
    path('observadosramitee', views.observadosramite, name='observadosramite'),

      path('tramite/tarjeta_tramite/<int:id>', views.tarjeta_tramite, name='tarjeta_tramite'),
  path('generar_licencia_pdf/<int:id>',views.generar_licencia_pdf, name='generar_licencia_pdf'),
    path('descargarDetalleCompleto/<int:id>',views.descargarDetalleCompleto, name='descargarDetalleCompleto'),
    path('verificarPago/<int:id>',views.verificarPago, name='verificarPago'),
        path('crearRuta',views.crearRuta, name='crearRuta'),
  
   path('listarRuta',views.listarRuta, name='listarRuta'),
      path('tramitesVigentes',views.tramitesVigentes, name='tramitesVigentes'),
        path('crearCosto',views.crearCosto, name='crearCosto'),
           path('listarCosto',views.listarCosto, name='listarCosto'),
               path('eliminarCosto/<int:id>',views.eliminarCosto, name='eliminarCosto'),
              path('editarCosto/<int:id>',views.editarCosto, name='editarCosto')
  
  

  


]

