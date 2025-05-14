from django.shortcuts import redirect, render,get_object_or_404
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
            return redirect(reverse('listarFedeacion'))
            

    else:
        operador=OperadorF()
        context={'operador':operador}
        return render(request,'operador/crear.html', context)
    

def editar_operador(request, ope_id):
    ope = get_object_or_404(Operador, id= ope_id)

    if request.method == 'POST':
        form = OperadorF(request.POST, instance=ope)
        if form.is_valid():
            form.save()
            return redirect('listarOperador')  
    else:
        form = OperadorF(instance=ope)
        

    return render(request, 'operador/editar.html', {'form': form,'id':ope.id})


def eliminar_operador(request, ope_id):
    operador = get_object_or_404(Operador, id=ope_id)
    operador.flag = False
    operador.save()
    return redirect('listarOperador')