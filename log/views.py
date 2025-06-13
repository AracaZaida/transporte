from django.shortcuts import render

from log.models import Log
from utils.context_processors import verificarRol
from django.contrib.auth.decorators import login_required
from datetime import date




@login_required
def registrar_log(request,modelo,usuario,descripcion):
    Log.objects.create(modelo=modelo, usuario=usuario, descripcion=descripcion)
    return
@login_required


def listar_log(request):
       
    resultado = verificarRol(request, ['super_admin'])
    if resultado is not True:
        return resultado

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    filtros = {}

 
    if fecha_inicio and fecha_fin:
        filtros['fecha_creacion__date__gte'] = fecha_inicio
        filtros['fecha_creacion__date__lte'] = fecha_fin
    else:
        hoy = date.today()
        filtros['fecha_creacion__date'] = hoy
     
    log= Log.objects.filter(**filtros)
    return render(request, 'log/listar.html', {
    'log': log,
    'today': date.today()
    })
    