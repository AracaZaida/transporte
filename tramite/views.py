from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from tramite.forms import Tipo_tramiteF, TramiteF
from tramite.models import Tramite
from vehiculo.forms import VehiculosF
from datetime import date


def crearTramite(request):
    if request.method =='POST':
        tramite=TramiteF(request.POST)
        vehiculos=VehiculosF(request.POST)
        if tramite.is_valid() and vehiculos.is_valid():
            fecha_validezI = tramite.cleaned_data['fecha_validezI']
            fecha_validezF =fecha_validezI.replace(year=fecha_validezI.year + 1)
            vehi=vehiculos.save()
            trami=tramite.save(commit=False)
            trami.vehiculo=vehi
            trami.fecha_validezF= fecha_validezF
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

def crearTipo_tramite(request):
    if request.method =='POST':
        tipo_tramite=Tipo_tramiteF(request.POST)
        if tipo_tramite.is_valid():
            tipo_tramite.save()
        
            return redirect(reverse('listarTramite'))
            

    else:
        tipo_tramite=Tipo_tramiteF()
        context={'tipo_tramite': tipo_tramite}

        return render(request,'tramite/crearTipoTramite.html', context)
def detalleTramite (request, id):
    detalle = get_object_or_404(Tramite, pk=id)

    context  = {
        'tramite':detalle
    }
    return render(request,'tramite/detalleTramite.html', context)