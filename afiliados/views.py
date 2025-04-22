from django.shortcuts import render, redirect
from django.http import HttpResponse

from utils.context_processors import verificarRol
from .forms import Afiliados
from django.urls import reverse

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Afiliado


def afiliadoLista(request):
    resultado = verificarRol(request, ['super_admin','administrador'])
        
    if resultado is not True:
        return resultado
    afiliados = Afiliado.objects.all()
    context={'afiliados':afiliados}

    return render(request, 'afiliados/afiliados.html', context)

def crearAfiliados(request):
    resultado = verificarRol(request, ['super_admin','administrador'])
        
    if resultado is not True:
        return resultado
    if request.method =='POST':
        afiliados=Afiliados(request.POST)
        if afiliados.is_valid():
            afiliados.save()
            return redirect(reverse('afiliadoLista'))
            

    else:
        afiliados=Afiliados()
        context={'afiliados':afiliados}
        return render(request,'afiliados/crear.afiliados.html', context)

