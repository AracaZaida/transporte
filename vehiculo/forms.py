from django import forms
from .models import Vehiculo

class VehiculosF(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['marca', 'modelo', 'tipo_vehiculo', 'placa', 'color', 'afiliado', 'chasis', 'tipo_transporte', 'capacidad']
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_vehiculo': forms.TextInput(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'afiliado': forms.Select(attrs={'class': 'form-select'}),
            'chasis': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_transporte': forms.Select(attrs={'class': 'form-select'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }
