from django import forms
from .models import Tipo_tramite, Tramite
class TramiteF(forms.ModelForm):
    class Meta:
        model = Tramite
        fields= ['gestion','rutasOperar','fecha_validezI','estado','monto','observaciones','fecha_entrega','numero_fojas','numero_deposito','tipo_tramite']
        widgets = {
            'gestion': forms.TextInput(attrs={'class': 'form-control'}),
            'rutasOperar': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha_validezI': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_entrega': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'numero_fojas': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_deposito': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_tramite': forms.Select(attrs={'class': 'form-control'}),
        }

class Tipo_tramiteF(forms.ModelForm):
    class Meta:
        model= Tipo_tramite
        fields=['nombre']
