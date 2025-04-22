from django.shortcuts import render,redirect
from django.urls import reverse

from .models import Usuario
from usuarios.forms import UsuarioF
from django.contrib.auth import authenticate , login
from django.contrib import messages
from utils.context_processors import verificarRol
def listarUsuario(request):
    resultado = verificarRol(request, ['super_admin'])
    if resultado is not True:
        return resultado
    usuario = Usuario.objects.all()
    context={'usuario':usuario}

    return render(request, 'usuario/listar.html', context)

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
                return redirect(reverse('home'))
            else:
                messages.error(request, 'Usuario o contraseña incorrectos')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
                
    return render(request,'usuario/login.html')

    
def home(request):            
    return render(request,'usuario/home.html')