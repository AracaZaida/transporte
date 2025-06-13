from django import forms
from operador.models import Operador

class OperadorF(forms.ModelForm):
    class Meta:
        model = Operador
        fields = ['nombre', 'direccion', 'celular', 'federacion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del operador'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la dirección'
            }),
            'celular': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el número de celular'
            }),
            'federacion': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        # Capitaliza nombre y direccion
        nombre = cleaned_data.get('nombre')
        direccion = cleaned_data.get('direccion')

        if nombre:
            cleaned_data['nombre'] = nombre.title()

        if direccion:
            cleaned_data['direccion'] = direccion.title()

        return cleaned_data

