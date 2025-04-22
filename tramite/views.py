from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from tramite.models import Tramite
from utils.context_processors import verificarRol
from vehiculo.models import Vehiculo
from datetime import  datetime

from usuarios.models import Usuario

from  afiliados.models import Afiliado

from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from .models import Tramite, Usuario, Afiliado

def crearTramite(request):
    resultado = verificarRol(request, ['super_admin','administrador'])
    if resultado is not True:
        return resultado
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        fecha_validezI = request.POST.get('fecha')
        afiliado_id = request.POST.get('afiliado_id')
        tecnico_id = request.POST.get('tecnico_id')

        if tipo and fecha_validezI and afiliado_id and tecnico_id:
            # Convertir fecha de string a objeto datetime.date
            fecha_validezI = datetime.strptime(fecha_validezI, '%Y-%m-%d').date()
            fecha_validezF = fecha_validezI.replace(year=fecha_validezI.year + 1)
            gestion = datetime.now().year

            # Obtener objetos relacionados
            afiliado = Afiliado.objects.get(id=afiliado_id)
            tecnico = Usuario.objects.get(id=tecnico_id)

            Tramite.objects.create(
                tipo_tramite=tipo,
                fecha_validezI=fecha_validezI,
                fecha_validezF=fecha_validezF,
                gestion=gestion,
                afiliado=afiliado,
                usuario=tecnico
            )

            return redirect(reverse('listarTramite'))
        else:
         
            print("Datos incompletos")


    tecnicos = Usuario.objects.filter(rol='tecnico', es_activo=True)
    afiliados = Afiliado.objects.filter(flag='nuevo')
    context = {
        'tecnicos': tecnicos,
        'afiliados': afiliados
    }
    return render(request, 'tramite/crearTramite.html', context)

    
def verTramite(request, id):
    resultado = verificarRol(request, ['super_admin','administrador','tecnico'])
    if resultado is not True:
        return resultado
    tramite = get_object_or_404(Tramite, pk=id)

    if request.method =='POST':
            estado = request.POST.get('estado')
            detalle = request.POST.get('detalle')
            tramite.estado = estado
            tramite.observaciones = detalle
            tramite.save()
            return redirect(reverse('listarTramite'))
    else:
       
        context={'id':id,'tramite':tramite}

        return render(request,'tramite/verTramite.html', context)

def listarTramite(request):
    resultado = verificarRol(request, ['tecnico','administrador'])
    if resultado is not True:
        return resultado
    tramite = Tramite.objects.filter(flag='nuevo', estado='ingresado')
    context={'tramite':tramite}
    return render(request, 'tramite/listarT.html', context)

def verificadoTramite(request):
    resultado = verificarRol(request, ['super_admin','administrador'])
    if resultado is not True:
        return resultado
    tramite = Tramite.objects.filter(flag='nuevo', estado='verificado')
    context={'tramite':tramite}
    return render(request, 'tramite/verificado.html', context)

def observadosramite(request):
    resultado = verificarRol(request, ['super_admin','administrador'])
    if resultado is not True:
        return resultado
    tramite = Tramite.objects.filter(flag='nuevo', estado='observado')
    context={'tramite':tramite}
    return render(request, 'tramite/observado.html', context)


def detalleTramite (request, id):
    detalle = get_object_or_404(Tramite, pk=id)

    context  = {
        'tramite':detalle
    }
    return render(request,'tramite/detalleTramite.html', context)

def tarjeta_tramite (request, id):
    resultado = verificarRol(request, ['super_admin','administrador'])
    if resultado is not True:
        return resultado
    tramite = get_object_or_404(Tramite, pk=id)
    if request.method =='POST':
        placa = request.POST.get('placa')
        tipo_transporte = request.POST.get('tipo_transporte')
        modelo = request.POST.get('modelo')
        marca = request.POST.get('marca')
        chasis = request.POST.get('chasis')
        tipo_servicio = request.POST.get('tipo_servicio')
        capacidad = request.POST.get('capacidad')
        rutas_autorizadas = request.POST.get('rutas_autorizadas')
        monto = request.POST.get('monto')

        Vehiculo.objects.create(marca= marca, 
                                modelo = modelo,
                                 placa= placa, 
                                 tipo_transporte =tipo_transporte,
                                 chasis= chasis,
                                 capacidad= capacidad,
                                 afiliado= tramite.afiliado,
                                tipo_vehiculo=tipo_servicio
                                 )
        tramite.monto = monto
        tramite.rutasOperar = rutas_autorizadas
        tramite.save()

    context  = {
        'tramite':tramite
    }
    return render(request,'tramite/tarjeta.html', context)

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