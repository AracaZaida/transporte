from django import forms
from .models import Tramite
class TramiteF(forms.ModelForm):
    class Meta:
        model = Tramite
        fields= ['gestion','rutasOperar','fecha_validezI','estado','monto']
        widgets = {
            'fecha_validezI': forms.DateInput(attrs={'type': 'date'}),
        }