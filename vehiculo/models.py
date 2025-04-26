from django.db import models
from afiliados.models import Afiliado 

class Vehiculo(models.Model):
    marca=models.CharField(max_length=50, blank=False, null=False)
    color=models.CharField(max_length=50, blank=False, null=False)
    modelo=models.CharField(max_length=100, blank=False, null=False)
    placa=models.CharField(max_length=50, blank=False, null=False)
    tipo_transporte= models.CharField(max_length=20,
        choices=[('carga', 'carga'), ('pasajero', 'pasajero')])
    chasis=models.CharField(max_length=255, blank=True, null=True)
    capacidad=models.CharField(max_length=255, blank=True, null=True)
  
    tipo_vehiculo=models.CharField(max_length=100, blank=False, null=False)
    fecha_creacion = models.DateField(auto_now_add=True)
    flag=models.CharField(max_length=20,
        choices=[('nuevo', 'nuevo'), ('eliminado', 'eliminado')],
        default='nuevo')
     
    def __str__(self):
        return f"{self.marca} {self.modelo} {self.placa}"