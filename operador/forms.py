from django import forms

from operador.models import Operador

class OperadorF(forms.ModelForm):
    class Meta:
        model = Operador
        fields= ['nombre','direccion','celular','federacion']

