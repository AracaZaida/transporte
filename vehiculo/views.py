from django.shortcuts import render,redirect
from django.urls import reverse

from utils.context_processors import verificarRol
from vehiculo.models import Vehiculo
from .forms import VehiculosF


def crearVehiculo(request):
    resultado = verificarRol(request, ['super_admin','administrador'])
        
    if resultado is not True:
        return resultado
    if request.method =='POST':
        vehiculo=VehiculosF(request.POST)
        if vehiculo.is_valid():
            vehiculo.save()
            return redirect(reverse('afiliadoLista'))
            

    else:
        vehiculo=VehiculosF()
        context={'vehiculo':vehiculo}
        return render(request,'vehiculo/crearVehiculo.html', context)
    
def listaVehiculo(request):
    resultado = verificarRol(request, ['super_admin','administrador'])
        
    if resultado is not True:
        return resultado
    vehiculo = Vehiculo.objects.all()
    context={'vehiculo':vehiculo}

    return render(request, 'vehiculo/listarVehiculo.html', context)

