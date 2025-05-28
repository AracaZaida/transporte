from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse

from log.views import registrar_log

from .models import Usuario
from usuarios.forms import UsuarioF, UsuariosActualizar
from django.contrib.auth import authenticate , login, logout
from django.contrib import messages
from utils.context_processors import verificarRol
from django.contrib.auth.decorators import login_required


@login_required
def listarUsuario(request):
    resultado = verificarRol(request, ['super_admin'])
    if resultado is not True:
        return resultado
    usuario = Usuario.objects.filter(es_habilitado=True)
    context={'usuario':usuario}

    return render(request, 'usuario/listar.html', context)

@login_required
def crearUsuario(request):
    resultado = verificarRol(request, ['super_admin'])
    if resultado is not True:
        return resultado
    
    if request.method =='POST':
        usuario=UsuarioF(request.POST)
  
        if usuario.is_valid():
            password = usuario.cleaned_data['password']
            u =  usuario.save(commit=False)
            u.set_password(password)
            u.save()
            registrar_log(request,'usuario',request.user.username, f'se regitro el usuario  {usuario.cleaned_data['username']}')
            return redirect(reverse('listarUsuario'))
        else:
            context = {'usuario': usuario}
            return render(request, 'usuario/crearUsusario.html', context)
    else:
        usuario=UsuarioF()
        context={'usuario':usuario}
        return render(request,'usuario/crearUsusario.html', context)
    
def login_sistema(request):
    
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
      
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                registrar_log(request,'usuario',username, f'se logueo el usuario {username}')
                return redirect(reverse('home'))
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
                
    return render(request,'usuario/login.html')


def home(request):            
    return render(request,'usuario/home.html')

@login_required
def editar_user(request, usu_id):
    resultado = verificarRol(request, ['super_admin'])
    if resultado is not True:
        return resultado
    user = get_object_or_404(Usuario, id=usu_id)

    if request.method == 'POST':
        form = UsuariosActualizar(request.POST, instance=user)
        if form.is_valid():
            form.save()
            registrar_log(request,'usuario',request.user.username, f'se edito el usuario {user.username}')
            return redirect('listarUsuario')  
    else:
        form = UsuariosActualizar(instance=user)
        

    return render(request, 'usuario/editar.html', {'form': form,'id':user.id})

@login_required
def eliminar_usuario(request, usuario_id):
    resultado = verificarRol(request, ['super_admin'])
    if resultado is not True:
        return resultado
    user = get_object_or_404(Usuario, id=usuario_id)
    user.es_activo = False
    user.es_habilitado = False
    user.save()
    registrar_log(request,'usuario',request.user.username, f'se elimino el usuario {user.username}')
    return redirect('listarUsuario')
@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('login')