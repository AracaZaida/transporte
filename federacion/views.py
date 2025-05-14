from django.shortcuts import render,redirect, get_object_or_404
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
    
def editar_federacion(request, fer_id):
    fed= get_object_or_404(Federacion, id= fer_id)

    if request.method == 'POST':
        form = Federacions(request.POST, instance=fed)
        if form.is_valid():
            form.save()
            return redirect('listarFedeacion')  
    else:
        form = Federacions(instance=fed)
        

    return render(request, 'federacion/editar.html', {'form': form,'id':fed.id})

def eliminar_federacion(request, fer_id):
    fer = get_object_or_404(Federacion, id=fer_id)
    fer.flag = False
    fer.save()
    return redirect('listarFedeacion')


