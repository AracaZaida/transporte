from django.db import models

from afiliados.models import Afiliado
from federacion.models import Federacion
from operador.models import Operador
from usuarios.models import Usuario
from vehiculo.models import Vehiculo


class Rutas(models.Model):
    nombre=models.TextField(null=True, blank=True)


class Tramite(models.Model):
    gestion=models.CharField(max_length=100, blank=False, null=False)
    numero_tramite = models.IntegerField(blank=True ,null=True)
    numero_fojas=models.IntegerField(blank=True ,null=True)
    fecha_validezI=models.DateField()
    fecha_validezF=models.DateField(blank=True, null=True)
    numero_comprobante=models.CharField(blank=True, null=True)
    verificarPago=models.BooleanField(default=False)
    monto = models.IntegerField(default=0)
    observaciones = models.TextField(null=True, blank=True)
    tipo_tramite= models.CharField(max_length=100,blank=False, null=False)
    fecha_pago = models.DateField(blank=True, null=True)
    operador = models.ForeignKey(Operador, on_delete=models.CASCADE, blank=False, null=False)
    estado = models.CharField(max_length=50,
            choices=[('verificado', 'verificado'), ('observado', 'observado'),('ingresado','ingresado')],
        default='ingresado')
    usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

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

class DetalleTramite(models.Model):
    rutas=models.CharField(blank=True, null=True)#models.ForeignKey(Rutas, on_delete=models.CASCADE, blank=False, null=False)
    vehiculo=models.ForeignKey(Vehiculo, on_delete=models.CASCADE, blank=False, null=False)
    afiliado = models.CharField(blank=True, null=True)  #models.ForeignKey(Afiliado, on_delete=models.CASCADE, blank=False, null=False)
    tramite = models.ForeignKey(Tramite, on_delete=models.CASCADE, blank=False, null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    flag=models.CharField(max_length=20,
        choices=[('nuevo', 'nuevo'), ('eliminado', 'eliminado')],
        default='nuevo')
    