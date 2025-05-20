from django.shortcuts import render

from log.models import Log
from utils.context_processors import verificarRol

def registrar_log(modelo,usuario,descripcion):
    Log.objects.create(modelo=modelo, usuario=usuario, descripcion=descripcion)
    return
def listar_log(request):
     
    resultado = verificarRol(request, ['super_admin'])
    if resultado is not True:
        return resultado
    log= Log.objects.all()
    return render(request, 'log/listar.html', {'log': log})
    