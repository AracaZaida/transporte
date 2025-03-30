from django import forms
from .models import Federacion
class Federacions(forms.ModelForm):
    class Meta:
        model = Federacion
        fields= ['nombre']