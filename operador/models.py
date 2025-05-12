from django.db import models

from federacion.models import Federacion


class Operador(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    direccion=models.CharField(max_length=100, blank=False, null=False)
    celular=models.CharField(max_length=100, blank=False, null=False)
    federacion = models.ForeignKey(Federacion, on_delete=models.CASCADE, blank=False, null=False)
    fecha_creacion = models.DateField(auto_now_add=True)
    flag=models.CharField(max_length=20,
        choices=[('nuevo', 'nuevo'), ('eliminado', 'eliminado')],
        default='nuevo')
    def __str__(self):
        return f"{self.nombre}"