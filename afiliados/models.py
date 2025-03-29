from django.db import models

from django.db import models

class Afiliado(models.Model):
    nombre = models.CharField(max_length=100, blank=False, null=False)
    apellido = models.CharField(max_length=100,blank=False, null=False)
    carnet= models.CharField(max_length=100,blank=False, null=False)
    email = models.EmailField()
    celular = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    fecha_afiliacion = models.DateField(auto_now_add=True)
    flag=models.CharField(max_length=20,
        choices=[('nuevo', 'nuevo'), ('eliminado', 'eliminado'),],
        default='nuevo')
    estado_afiliacion = models.CharField(
        max_length=20,
        choices=[('activo', 'Activo'), ('inactivo', 'Inactivo'), ('suspendido', 'Suspendido')],
        default='activo'
    )
    
    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.numero_afiliado})"

