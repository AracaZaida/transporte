from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Usuario
from usuarios.forms import UsuarioF
def listarUsuario(request):
    
    usuario = Usuario.objects.all()
    context={'usuario':usuario}

    return render(request, 'usuario/listar.html', context)

def crearUsuario(request):
    if request.method =='POST':
        usuario=UsuarioF(request.POST)
        if usuario.is_valid():
            usuario.save()
            return redirect(reverse('listarUsuario'))
            

    else:
        usuario=UsuarioF()
        context={'usuario':usuario}
        return render(request,'usuario/crearUsusario.html', context)