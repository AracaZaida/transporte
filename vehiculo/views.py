import json
from django.http import JsonResponse 
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from tramite.models import DetalleTramite
from utils.context_processors import verificarRol
from vehiculo.models import Marca, Vehiculo
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


@login_required        
def listarVehiculos(request):
    data = []
    vehiculos = Vehiculo.objects.filter(flag='nuevo')

    for v in vehiculos:
        tramite = DetalleTramite.objects.filter(vehiculo=v.pk, flag='nuevo')
        for t in tramite:
            d = {
                'federacion': t.tramite.operador.federacion.nombre,
                'operador': t.afiliado,
                'marca': v.marca,
                'modelo': v.modelo,
                'placa': v.placa,
                'tipo_transporte': v.tipo_transporte,
                'chasis': v.chasis,
                'capacidad': v.capacidad,
                'idTramite': t.pk,
                'idAuto': v.pk
            }
            data.append(d)

    
    paginator = Paginator(data, 10) 
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)

    return render(request, 'vehiculo/listarVehiculo.html', {'page_obj': page_obj})

@login_required        
def eliminarVehiculo(request, id):
    detalleTratamite = get_object_or_404(DetalleTramite,pk=id)
    detalleTratamite.flag='eliminado'
    detalleTratamite.vehiculo.flag='eliminado'
    detalleTratamite.vehiculo.save()
    detalleTratamite.save()
    return redirect('listarTrasnporte')