from django.shortcuts import redirect, render
from django.urls import reverse

from operador.forms import OperadorF
from operador.models import Operador

def listarOperador(request):
    
    operador = Operador.objects.filter(flag='nuevo')
    context={'operador':operador}

    return render(request, 'operador/listar.html', context)
# Create your views here.
def crearOperdor(request):
    if request.method =='POST':
        operador=OperadorF(request.POST)
        if operador.is_valid():
            operador.save()
            return redirect(reverse('listarOperador'))
            

    else:
        operador=OperadorF()
        context={'operador':operador}
        return render(request,'operador/crear.html', context)