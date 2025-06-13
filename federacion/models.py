from django.db import models



class Federacion(models.Model):
   nombre = models.CharField(max_length=100, blank=False, null=False)
   direccion=models.CharField(max_length=100, blank=False, null=False)
   celular = models.CharField(max_length=15, blank=True, null=True)
   fecha_creacion = models.DateField(auto_now_add=True)
   flag=models.CharField(max_length=20,
        choices=[('nuevo', 'nuevo'), ('eliminado', 'eliminado')],
        default='nuevo')
     
   def __str__(self):
         return f"{self.nombre}"
