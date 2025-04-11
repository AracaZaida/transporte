from django.db import models

from afiliados.models import Afiliado
from usuarios.models import Usuario
from vehiculo.models import Vehiculo



class Tramite(models.Model):
    gestion=models.CharField(max_length=100, blank=False, null=False)
   # rutasOperar=models.TextField(max_length=100, blank=False, null=False)
    fecha_validezI=models.DateField()
    fecha_validezF=models.DateField(blank=True, null=True)
    #numero_deposito=models.CharField(max_length=100, blank=True, null=True)
    #monto = models.DecimalField(max_digits=10, decimal_places=2)
    afiliado=models.ForeignKey(Afiliado, on_delete=models.CASCADE)
    #observaciones = models.TextField(null=True, blank=True)
    tipo_tramite= models.CharField(max_length=100,blank=False, null=False)
    
    estado = models.CharField(max_length=50,
            choices=[('verificado', 'verificado'), ('observado', 'observado'),('derivado','derivado'),('derivar','derivar')],
        default='verificado')
    usuario=models.ForeignKey(Usuario, on_delete=models.CASCADE)


    fecha_creacion = models.DateField(auto_now_add=True)
    flag=models.CharField(max_length=20,
        choices=[('nuevo', 'nuevo'), ('eliminado', 'eliminado')],
        default='nuevo')
    
