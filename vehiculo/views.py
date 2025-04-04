from django.shortcuts import render,redirect
from django.urls import reverse

from vehiculo.models import Vehiculo
from .forms import VehiculosF


def crearVehiculo(request):
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
    
    vehiculo = Vehiculo.objects.all()
    context={'vehiculo':vehiculo}

    return render(request, 'vehiculo/listarVehiculo.html', context)

