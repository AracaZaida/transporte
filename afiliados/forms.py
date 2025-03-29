from django import forms
from .models import Afiliado
class Afiliados(forms.ModelForm):
    class Meta:
        model = Afiliado
        fields= ['nombre','apellido','carnet','email','celular','direccion','fecha_afiliacion']