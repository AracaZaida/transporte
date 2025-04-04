from django.shortcuts import render,redirect
from django.urls import reverse


from tramite.forms import TramiteF
from tramite.models import Tramite
from vehiculo.forms import VehiculosF



def crearTramite(request):
    if request.method =='POST':
        tramite=TramiteF(request.POST)
        vehiculos=VehiculosF(request.POST)
        if tramite.is_valid() and vehiculos.is_valid():
            vehi=vehiculos.save()
            trami=tramite.save(commit=False)
            trami.vehiculo=vehi
            trami.save()
            return redirect(reverse('listarTramite'))
            

    else:
        tramite=TramiteF()
        vehiculo=VehiculosF()
        context={'tramite':tramite,'vehiculo':vehiculo}

        return render(request,'tramite/crearTramite.html', context)

def listarTramite(request):
    
    tramite = Tramite.objects.all()
    context={'tramite':tramite}

    return render(request, 'tramite/listarT.html', context)
