from django.db import models

class Usuario(models.Model):
    username=models.CharField(max_length=50, blank=True, null=True)
    ci=models.CharField(max_length=20,blank=True, null=False)
    nombre = models.CharField(max_length=50, null=False)
    apellidos = models.CharField(max_length=50, null=False)
    email = models.EmailField()
    contraseña=models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    rol = models.CharField(
        max_length=20,
        choices=[
            ('admin', 'Administrador'),
            ('operador', 'Operador'),
            ('personal', 'Personal'),
        ],
        default='cliente'
    )
    estado = models.BooleanField(default=True)

