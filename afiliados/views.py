from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import Afiliados
from django.urls import reverse

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Afiliado


def afiliadoLista(request):
    
    afiliados = Afiliado.objects.all()
    context={'afiliados':afiliados}

    return render(request, 'afiliados/afiliados.html', context)

def crearAfiliados(request):
    if request.method =='POST':
        afiliados=Afiliados(request.POST)
        if afiliados.is_valid():
            afiliados.save()
            return redirect(reverse('afiliadoLista'))
            

    else:
        afiliados=Afiliados()
        context={'afiliados':afiliados}
        return render(request,'afiliados/crear.afiliados.html', context)

