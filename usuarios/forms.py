from django import forms
from .models import Usuario

class UsuarioF(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['ci', 'nombre', 'apellidos', 'email', 'username', 'password', 'rol']
        widgets = {
            'ci': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }
    def clean(self):
        cleaned_data = super().clean()

        
        nombre = cleaned_data.get('nombre')
        apellidos = cleaned_data.get('apellidos')

       

        if nombre:
            cleaned_data['nombre'] = nombre.title()  

        if apellidos:
            cleaned_data['apellidos'] = apellidos.title()  

        return cleaned_data

class UsuariosActualizar(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['ci', 'nombre', 'apellidos', 'email', 'rol']
        widgets = {
            'ci': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }
    def clean(self):
        cleaned_data = super().clean()

        
        nombre = cleaned_data.get('nombre')
        apellidos = cleaned_data.get('apellidos')

       

        if nombre:
            cleaned_data['nombre'] = nombre.title()  

        if apellidos:
            cleaned_data['apellidos'] = apellidos.title()  

        return cleaned_data