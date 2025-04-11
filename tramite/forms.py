from django import forms
from .models import  Tramite
from usuarios.models import Usuario
class TramiteF(forms.ModelForm):
    class Meta:
        model = Tramite
        fields= ['fecha_validezI','estado','afiliado','tipo_tramite','usuario']
        widgets = {
            #'rutasOperar': forms.Textarea(attrs={'class': 'form-control','rows': 1}),
            'afiliado':forms.Select(attrs={'class': 'form-control'}),
            'fecha_validezI': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            #'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            #'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            #'numero_deposito': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_tramite': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(TramiteF,self).__init__(*args, **kwargs)
        tecnicos= [(usuario.id, usuario.username) for usuario in Usuario.objects.filter(rol='tecnico', es_habilitado=True )]
        self.fields['usuario'].widget = forms.Select(choices=tecnicos, attrs={'class': 'form-select'})
        self.fields['usuario'].widget.attrs.update({'class': 'form-select'})
        print(tecnicos)

