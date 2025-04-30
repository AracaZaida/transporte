from django.db import models

from afiliados.models import Afiliado
from usuarios.models import Usuario
from vehiculo.models import Vehiculo



class Tramite(models.Model):
    gestion=models.CharField(max_length=100, blank=False, null=False)
    numero_tramite = models.IntegerField(blank=True ,null=True)
    rutasOperar=models.TextField(null=True, blank=True)
    fecha_validezI=models.DateField()
    fecha_validezF=models.DateField(blank=True, null=True)
    #numero_deposito=models.CharField(max_length=100, blank=True, null=True)
    monto = models.IntegerField(default=0)
    afiliado=models.ForeignKey(Afiliado, on_delete=models.CASCADE)
    vehiculo=models.ForeignKey(Vehiculo, on_delete=models.CASCADE, blank=True, null=True)
    observaciones = models.TextField(null=True, blank=True)
    tipo_tramite= models.CharField(max_length=100,blank=False, null=False)
    
    estado = models.CharField(max_length=50,
            choices=[('verificado', 'verificado'), ('observado', 'observado'),('ingresado','ingresado')],
        default='ingresado')
    usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tiene_vehiculo = models.BooleanField(default=False)
    fecha_creacion = models.DateField(auto_now_add=True)
    flag=models.CharField(max_length=20,
        choices=[('nuevo', 'nuevo'), ('eliminado', 'eliminado')],
        default='nuevo')
    def save(self, *args, **kwargs):
        if not self.numero_tramite:
            ultimo_tramite = Tramite.objects.order_by('-id').first()

            if ultimo_tramite and ultimo_tramite.numero_tramite:
                nuevo_numero = str(int(ultimo_tramite.numero_tramite) + 1).zfill(4)
            else:
                nuevo_numero = "1000"
        
            self.numero_tramite = nuevo_numero
    
        super().save(*args, **kwargs)
