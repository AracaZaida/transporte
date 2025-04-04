from django.db import models

from vehiculo.models import Vehiculo

# Create your models here.
class Tramite(models.Model):
    gestion=models.CharField(max_length=100, blank=False, null=False)
    rutasOperar=models.TextField(max_length=100, blank=False, null=False)
    fecha_validezI=models.DateField()
    fecha_validezF=models.DateField(blank=True, null=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    vehiculo=models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    estado=models.CharField()
    fecha_creacion = models.DateField(auto_now_add=True)
    flag=models.CharField(max_length=20,
        choices=[('nuevo', 'nuevo'), ('eliminado', 'eliminado')],
        default='nuevo')
