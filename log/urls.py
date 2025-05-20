from . import views
from django.urls import path
urlpatterns = [
   path('listar_log',views.listar_log, name='listar_log'),
]
