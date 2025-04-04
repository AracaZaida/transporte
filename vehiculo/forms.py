from django import forms
from .models import Vehiculo
class VehiculosF(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields= ['marca','modelo','tipo_vehiculo','placa','color','afiliado','chasis','tipo_transporte','capacidad']