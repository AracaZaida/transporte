from . import views
from django.urls import path

urlpatterns = [
    path('crearMarca', views.crearMarca, name='crearMarca'),
      path('listarMarca', views.listarMarcas, name='listarMarcas'),

  path('listarTrasnporte', views.listarVehiculos, name='listarTrasnporte'),

]