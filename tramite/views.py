from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse
from federacion.models import Federacion
from operador.models import Operador
from tramite.models import Tramite ,Rutas
from utils.context_processors import verificarRol
from vehiculo.models import Vehiculo
from datetime import  datetime
import json
from usuarios.models import Usuario

from  afiliados.models import Afiliado

from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from .models import DetalleTramite, Tramite, Usuario, Afiliado
from django.http import HttpResponse, JsonResponse
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter

def crearTramite(request):
    resultado = verificarRol(request, ['super_admin','administrador'])
    if resultado is not True:
        return resultado
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        fecha_validezI = request.POST.get('fecha')
      
        tecnico_id = request.POST.get('tecnico_id')
        operador = request.POST.get('afiliado_id')
        fojas=request.POST.get('fojas')

        if tipo and fecha_validezI  and tecnico_id:
            # Convertir fecha de string a objeto datetime.date
            fecha_validezI = datetime.strptime(fecha_validezI, '%Y-%m-%d').date()
            fecha_validezF = fecha_validezI.replace(year=fecha_validezI.year + 1)
            gestion = datetime.now().year
            operador = get_object_or_404(Operador, pk= operador)
            # Obtener objetos relacionados
         
            tecnico = Usuario.objects.get(id=tecnico_id)

            Tramite.objects.create(
                tipo_tramite=tipo,
                fecha_validezI=fecha_validezI,
                fecha_validezF=fecha_validezF,
                gestion=gestion,
               operador=operador,
                usuario=tecnico,
                numero_fojas= fojas
            )

            return redirect(reverse('listarTramite'))
        else:
         
            print("Datos incompletos")


    tecnicos = Usuario.objects.filter(rol='tecnico', es_activo=True)
   # afiliados = Afiliado.objects.filter(flag='nuevo')
    operador = Operador.objects.filter(flag='nuevo')
    context = {
        'tecnicos': tecnicos,
         'operador': operador,
       # 'afiliados': afiliados
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
    tramite = get_object_or_404(Tramite, pk=id)
    detalle = DetalleTramite.objects.filter(tramite= tramite)
    context  = {
        'tramite':tramite,
        'detalle':detalle
    }
    return render(request,'tramite/detalleTramite.html', context)

def tarjeta_tramite (request, id):
    resultado = verificarRol(request, ['super_admin','administrador'])
    if resultado is not True:
        return resultado
    tramite = get_object_or_404(Tramite, pk=id)
    if request.method =='POST':
        data = json.loads(request.body)
        for d in data:
            afiliado = get_object_or_404(Afiliado, pk =  d["afiliado_id"])
            ruta = get_object_or_404(Rutas, pk=d["ruta_id"])
            vehiculo=Vehiculo.objects.create(marca= d["marca"], 
                                
                                modelo = d["modelo"],
                                 placa= d["placa"], 
                                 tipo_transporte =d["tipo_transporte"],
                                 chasis= d["chasis"],
                                 capacidad= d["capacidad"],
                                 
                                tipo_vehiculo=d["tipo_servicio"]
                                 )
        
            DetalleTramite.objects.create(vehiculo= vehiculo , rutas=ruta , afiliado= afiliado, tramite= tramite)
        print('registrado')
        return JsonResponse({"status": "success"}, status=201)
    afiliado = Afiliado.objects.filter(federacion = tramite.operador.federacion)
    context  = {
        'tramite':tramite,
        'afiliados':afiliado
    }
    return render(request,'tramite/tarjeta.html', context)

def editarTramite(request, id):
    tramite = get_object_or_404(DetalleTramite, pk=id)
    
    if request.method =='POST':
        ruta = request.POST.get('ruta_id')    
        r = get_object_or_404(Rutas, pk= ruta)
        placa = request.POST.get('placa')
        tipo_transporte = request.POST.get('tipo_transporte')
        modelo = request.POST.get('modelo')
        marca = request.POST.get('marca')
        chasis = request.POST.get('chasis')
        tipo_servicio = request.POST.get('tipo_servicio')
        capacidad = request.POST.get('capacidad')
        
    
        tramite.vehiculo.placa = placa
        tramite.vehiculo.tipo_transporte= tipo_transporte
        tramite.vehiculo.modelo = modelo
        tramite.vehiculo.marca = marca
        tramite.vehiculo.chasis =chasis
        tramite.vehiculo.tipo_vehiculo = tipo_servicio
        tramite.vehiculo.capacidad = capacidad
        tramite.rutas= r
        tramite.vehiculo.save()
        tramite.save()
        return redirect(reverse('verificadoTramite'))

    context  = {
        'tramite':tramite
    }
    return  render(request,'tramite/editarTramite.html',context)

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

def verificarPago(request, id):
    tramite = get_object_or_404(Tramite, pk= id)
    if request.method =='POST':
        
        numeroComprobante = request.POST.get('numeroComprobante')
        fechaPago = request.POST.get('fechaPago')
        monto = request.POST.get('monto')
        tramite.numero_comprobante= numeroComprobante
        tramite.fecha_pago= fechaPago
        tramite.monto = monto
        tramite.verificarPago= True
        tramite.save()
        return redirect(reverse('verificadoTramite'))
    return render(request, 'tramite/verificarPago.html', {'id':tramite.id})

def crearRuta(request):  # Usa el `id` si lo necesitas
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            if not nombre:
                return JsonResponse({'estatus': 400, 'mensaje': 'Nombre requerido'}, status=400)
            Rutas.objects.create(nombre=nombre)
            return JsonResponse({'estatus': 201})
        except Exception as e:
            return JsonResponse({'estatus': 500, 'mensaje': str(e)}, status=500)
def listarRuta(request):
    rutas = Rutas.objects.all()  
    rutas_data = list(rutas.values('id', 'nombre'))  
    return JsonResponse(rutas_data, safe=False)

def generar_licencia_pdf(request, id):
    detalle=get_object_or_404(DetalleTramite, pk=id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="licencia_operacion.pdf"'

    width, height = letter
    height = height / 2  
    p = canvas.Canvas(response, pagesize=(width, height))

    p.setLineWidth(0.5)
    p.rect(30, 20, width - 60, height - 40)

    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(width / 2, height - 35, "LICENCIA DE OPERACIÓN PARA EL TRANSPORTE AUTOMOTOR")
    p.drawCentredString(width / 2, height - 50, "INTERPROVINCIAL - CONFEDERADO")

    p.setStrokeColor(colors.grey)
    p.line(40, height - 60, width - 40, height - 60)

    y = height - 75
    p.setFont("Helvetica-Bold", 8)
    p.drawString(50, y, "Línea Sindical:")
    p.setFont("Helvetica", 8)
    p.drawString(140, y, f"{detalle.afiliado.federacion.nombre}")
    y -= 18

    datos_col1 = [
        ("Operador:", f"{detalle.afiliado.nombre } {detalle.afiliado.apellido}"),
        ("Afiliado:", f"{detalle.afiliado.id}"),
        ("Modelo:", f"{detalle.vehiculo.modelo}"),
        ("Registro:", f"{detalle.tramite.numero_tramite}"),
    ]
    datos_col2 = [
        ("Categoría:", f"{detalle.vehiculo.tipo_vehiculo}"),
        ("Capacidad:", f"{detalle.vehiculo.capacidad}"),
        ("Chasis:", f"{detalle.vehiculo.chasis}"),
        ("Marca:", f"{detalle.vehiculo.marca}"),
    ]
    x1 = 50
    x2 = width / 2 + 10
    for i in range(4):
        p.setFont("Helvetica-Bold", 8)
        p.drawString(x1, y, datos_col1[i][0])
        p.setFont("Helvetica", 8)
        p.drawString(x1 + 90, y, datos_col1[i][1])

        p.setFont("Helvetica-Bold", 8)
        p.drawString(x2, y, datos_col2[i][0])
        p.setFont("Helvetica", 8)
        p.drawString(x2 + 80, y, datos_col2[i][1])
        y -= 14

    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.black)
    p.drawCentredString(width / 2, y - 10, f"{detalle.vehiculo.placa}")
    y -= 25

    p.setStrokeColor(colors.black)
    p.line(40, y, width - 40, y)
    y -= 12

    p.setFont("Helvetica-Bold", 8)
    p.drawString(50, y, "Rutas Autorizadas:")
    p.setFont("Helvetica", 8)
    y -= 12
    p.drawString(70, y, f"{detalle.rutas.nombre}")
    y -= 12
 
    p.setFont("Helvetica-Bold", 8)
    p.drawString(50, y, "Licencia válida de:")
    p.setFont("Helvetica", 8)
    p.drawString(140, y, f"{detalle.tramite.fecha_validezI} al {detalle.tramite.fecha_validezF}")
    y -= 18

    p.setFont("Helvetica", 7)
    p.drawRightString(width - 40, y, "Potosí - lunes, 24 de marzo de 2025")
    y -= 100

    p.setFont("Helvetica-Bold", 8)
    p.drawString(50, y, "Abog. Guido Soux Velasquez")
    p.setFont("Helvetica", 7)
    p.drawString(50, y - 10, "SECRETARIO DEPARTAMENTAL")
    p.drawString(50, y - 20, "DE JURÍDICA")

    p.setFont("Helvetica-Bold", 8)
    p.drawRightString(width - 50, y, "Oscar Mendoza Mamani")
    p.setFont("Helvetica", 7)
    p.drawRightString(width - 50, y - 10, "SECRETARIO DEPARTAMENTAL")
    p.drawRightString(width - 50, y - 20, "DE COORDINACIÓN GENERAL")

    p.showPage()
    p.save()

    return response
