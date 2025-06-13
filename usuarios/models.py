from django.db import models
from django.contrib.auth.models import AbstractBaseUser , UserManager, PermissionsMixin



from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

@receiver(post_migrate)
def crear_superadmin_por_defecto(sender, **kwargs):
    Usuario = get_user_model()
    if not Usuario.objects.filter(username='admin').exists():
        Usuario.objects.create(
            ci="0",
            nombre="Admin",
            apellidos="Principal",
            email="admin@example.com",
            username="admin",
            password=make_password("admin"), 
            rol="super_admin",
            es_habilitado=True,
           
        )

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
        default='super_admin'
    )
   
    USERNAME_FIELD = 'username'
    objects = UserManager()