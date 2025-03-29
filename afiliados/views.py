from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Afiliado


def afiliadoLista(request):
    
    afiliados = Afiliado.objects.all()
    context={'afiliados':afiliados}

    return render(request, 'afiliados/afiliados.html', context)

def crearAfiliados(resquest):
    if request.method =='POST':
        pass
    else:
        return render(request='afiliados/crear.afiliados.html')

