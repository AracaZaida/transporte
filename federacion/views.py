from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Federacion
from federacion.forms import Federacions
def listarFedeacion(request):
    
    federacion = Federacion.objects.filter(flag='nuevo')
    context={'federacion':federacion}

    return render(request, 'federacion/listar.html', context)

def crearFederacion(request):
    if request.method =='POST':
        federacion=Federacions(request.POST)
        if federacion.is_valid():
            federacion.save()
            return redirect(reverse('listarFedeacion'))
            

    else:
        federacion=Federacions()
        context={'federacion':federacion}
        return render(request,'federacion/crear.federacion.html', context)


