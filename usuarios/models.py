from django.db import models
from django.contrib.auth.models import AbstractBaseUser , UserManager, PermissionsMixin


class Usuario(AbstractBaseUser, PermissionsMixin):
    ci=models.CharField(max_length=20,blank=True, null=False)
    nombre = models.CharField(max_length=50, null=False)
    apellidos = models.CharField(max_length=50, null=False)
    email = models.EmailField()
    username= models.CharField(max_length=150, unique=True, blank=False, null=False, verbose_name='Usuario')
    password = models.CharField(max_length=128, blank=False, null=False, verbose_name='Contraseña')
    es_habilitado=models.BooleanField(default=True)
    es_activo=models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    rol = models.CharField(
        max_length=100,
        choices=[
            ('super_admin', 'super admin'),
            ('tecnico', 'tecnico'),
            ('administrador', 'administrador'),
        ],
        default='uper_admin'
    )
    
    USERNAME_FIELD = 'username'
    objects = UserManager()