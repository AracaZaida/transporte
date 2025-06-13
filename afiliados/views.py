from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse

from utils.context_processors import verificarRol
from .forms import Afiliados
from django.urls import reverse
from .models import Afiliado


def afiliadoLista(request):
    resultado = verificarRol(request, ['super_admin','administrador'])
        
    if resultado is not True:
        return resultado
    afiliados = Afiliado.objects.filter(flag='nuevo')
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
    


def editar_afiliado(request, afi_id):
    afili = get_object_or_404(Afiliado, id=afi_id)

    if request.method == 'POST':
        forms = Afiliados(request.POST, instance=afili)
        if forms.is_valid():
            forms.save()
            return redirect('afiliadoLista')
    else:
        forms = Afiliados(instance=afili)

    return render(request, 'afiliados/editar.html', {'forms': forms, 'id': afili.id})

def eliminar_afiliado(request, afi_id):
    afili = get_object_or_404(Afiliado, id=afi_id)
    afili.flag = 'eliminado'
    afili.save()
    return redirect('afiliadoLista')






