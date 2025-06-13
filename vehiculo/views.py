import json
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse

from utils.context_processors import verificarRol
from vehiculo.models import Marca
from django.contrib.auth.decorators import login_required




@login_required
def crearMarca(request):  # Usa el `id` si lo necesitas
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            if not nombre:
                return JsonResponse({'estatus': 400, 'mensaje': 'Nombre requerido'}, status=400)
            Marca.objects.create(nombre=nombre.title())
            return JsonResponse({'estatus': 201})
        except Exception as e:
            return JsonResponse({'estatus': 500, 'mensaje': str(e)}, status=500)
        
@login_required        
def listarMarcas(request):
    marca = Marca.objects.all()  
    marca_data = list(marca.values('id', 'nombre'))  
    return JsonResponse(marca_data, safe=False)