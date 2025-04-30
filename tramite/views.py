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
from django.http import HttpResponse
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

        vehiculo=Vehiculo.objects.create(marca= marca, 
                                
                                modelo = modelo,
                                 placa= placa, 
                                 tipo_transporte =tipo_transporte,
                                 chasis= chasis,
                                 capacidad= capacidad,
                                 
                                tipo_vehiculo=tipo_servicio
                                 )
        tramite.monto = int(monto)
        tramite.rutasOperar = rutas_autorizadas
        tramite.vehiculo=vehiculo
        tramite.tiene_vehiculo  = True
        tramite.save()
        return redirect(reverse('verificadoTramite'))
    context  = {
        'tramite':tramite
    }
    return render(request,'tramite/tarjeta.html', context)

def editarTramite(request, id):
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
        tramite.vehiculo.placa = placa
        tramite.vehiculo.tipo_transporte= tipo_transporte
        tramite.vehiculo.modelo = modelo
        tramite.vehiculo.marca = marca
        tramite.vehiculo.chasis =chasis
        tramite.vehiculo.tipo_vehiculo = tipo_servicio
        tramite.vehiculo.capacidad = capacidad
        tramite.rutasOperar= rutas_autorizadas
        tramite.monto = float(monto)
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




def generar_licencia_pdf(request, id):
    tramite=get_object_or_404(Tramite, pk=id)
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
    p.drawString(140, y, f"{tramite.afiliado.federacion.nombre}")
    y -= 18

    datos_col1 = [
        ("Operador:", f"{tramite.afiliado.nombre } {tramite.afiliado.apellido}"),
        ("Afiliado:", f"{tramite.afiliado.id}"),
        ("Modelo:", f"{tramite.vehiculo.modelo}"),
        ("Registro:", f"{tramite.numero_tramite}"),
    ]
    datos_col2 = [
        ("Categoría:", f"{tramite.vehiculo.tipo_vehiculo}"),
        ("Capacidad:", f"{tramite.vehiculo.capacidad}"),
        ("Chasis:", f"{tramite.vehiculo.chasis}"),
        ("Marca:", f"{tramite.vehiculo.marca}"),
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
    p.drawCentredString(width / 2, y - 10, f"{tramite.vehiculo.placa}")
    y -= 25

    p.setStrokeColor(colors.black)
    p.line(40, y, width - 40, y)
    y -= 12

    p.setFont("Helvetica-Bold", 8)
    p.drawString(50, y, "Rutas Autorizadas:")
    p.setFont("Helvetica", 8)
    y -= 12
    p.drawString(70, y, f"{tramite.rutasOperar}")
    y -= 12
 
    p.setFont("Helvetica-Bold", 8)
    p.drawString(50, y, "Licencia válida de:")
    p.setFont("Helvetica", 8)
    p.drawString(140, y, f"{tramite.fecha_validezI} al {tramite.fecha_validezF}")
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
