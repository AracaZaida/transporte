from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from tramite.forms import TramiteF
from tramite.models import Tramite
from vehiculo.forms import VehiculosF
from datetime import  datetime


def crearTramite(request):
    if request.method =='POST':
        fecha_actual = datetime.now()
        gestion = fecha_actual.year

        tramite=TramiteF(request.POST)
       
        if tramite.is_valid():
            fecha_validezI = tramite.cleaned_data['fecha_validezI']
            fecha_validezF =fecha_validezI.replace(year=fecha_validezI.year + 1)
           
            trami=tramite.save(commit=False)
            trami.gestion = gestion
            
            trami.fecha_validezF= fecha_validezF
            trami.save()
            return redirect(reverse('listarTramite'))
    else:
        tramite=TramiteF()
        vehiculo=VehiculosF()
        context={'tramite':tramite,'vehiculo':vehiculo}

        return render(request,'tramite/crearTramite.html', context)
    
def verTramite(request, id):
    tramite = get_object_or_404(Tramite, pk=id)

    if request.method =='POST':
        fecha_actual = datetime.now()
        gestion = fecha_actual.year
        tramite=TramiteF(request.POST, instance=tramite)
        if tramite.is_valid():
            fecha_validezI = tramite.cleaned_data['fecha_validezI']
            fecha_validezF =fecha_validezI.replace(year=fecha_validezI.year + 1)
           
            trami=tramite.save(commit=False)
            trami.gestion = gestion
            trami.fecha_validezF= fecha_validezF
            trami.save()
            return redirect(reverse('listarTramite'))
    else:
        tramite=TramiteF(instance=tramite)
        context={'tramite':tramite , 'id':id}

        return render(request,'tramite/verTramite.html', context)

def listarTramite(request):
    user = request.user
    
    if(user.rol == 'tecnico'):
        tramite = Tramite.objects.filter(flag='nuevo', usuario=user.id)
        context={'tramite':tramite, 'rol': user.rol}
        return render(request, 'tramite/listarT.html', context)
    else:
        tramite = Tramite.objects.filter(flag='nuevo')
        context={'tramite':tramite}
        return render(request, 'tramite/listarT.html', context)


def detalleTramite (request, id):
    detalle = get_object_or_404(Tramite, pk=id)

    context  = {
        'tramite':detalle
    }
    return render(request,'tramite/detalleTramite.html', context)
def aprobarTramite(request, id):
    tramite= get_object_or_404(Tramite, pk=id)
    tramite.estado ='aprobado'
    tramite.save()
    return redirect(reverse('listarTramite'))

def anularTramite(request, id):
    tramite= get_object_or_404(Tramite, pk=id)
    tramite.estado ='anulado'
    tramite.save()
    return redirect(reverse('listarTramite'))