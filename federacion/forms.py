from django import forms
from .models import Federacion

class Federacions(forms.ModelForm):
    class Meta:
        model = Federacion
        fields = ['nombre', 'direccion', 'celular']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la federación'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la dirección de la federación'
            }),
            'celular': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el número de celular'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        
        # Capitaliza nombre y dirección
        nombre = cleaned_data.get('nombre')
        direccion = cleaned_data.get('direccion')

        if nombre:
            cleaned_data['nombre'] = nombre.title()

        if direccion:
            cleaned_data['direccion'] = direccion.title()

        return cleaned_data
