from django import forms
from .models import Usuario
class UsuarioF(forms.ModelForm):
       class Meta:
        model = Usuario
        fields= ['ci','nombre','apellidos','email','username', 'password', 'rol' ]