from django.db import models

class Log(models.Model):
    modelo=models.CharField(null=False, blank=False, max_length=255)
    usuario=models.CharField(null=False, blank=False, max_length=255)
    descripcion=models.CharField(null=False, blank=False, max_length=255)
    fecha_creacion=models.DateTimeField(auto_now_add=True)

