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
from django.core.paginator import Paginator

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from io import BytesIO

from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

from django.utils import timezone

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
                numero_fojas= fojas,
                fecha_creacion=timezone.now()
            )

            return redirect(reverse('listarTramite'))
        else:
         
            print("Datos incompletos")


    tecnicos = Usuario.objects.filter(rol='tecnico', es_activo=True)
 
    operador = Operador.objects.filter(flag='nuevo')
    context = {
        'tecnicos': tecnicos,
         'operador': operador,
    
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
            if estado == 'verificado':
                tramite.fecha_verificacion = timezone.now()
            if estado == 'observado':
                tramite.fecha_observacion = timezone.now()
            tramite.save()
            return redirect(reverse('listarTramite'))
    else:
       
        context={'id':id,'tramite':tramite}

        return render(request,'tramite/verTramite.html', context)

def listarTramite(request):
    resultado = verificarRol(request, ['tecnico','administrador'])
    if resultado is not True:
        return resultado
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    filtros = {'flag': 'nuevo', 'estado': 'ingresado'}

 
    if fecha_inicio and fecha_fin:
        filtros['fecha_creacion__date__gte'] = fecha_inicio
        filtros['fecha_creacion__date__lte'] = fecha_fin

    tramite = Tramite.objects.filter(**filtros)


    paginator = Paginator(tramite, 20)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)  

   
    context = {'page_obj': page_obj}
    return render(request, 'tramite/listarT.html', context)
def verificadoTramite(request):
    resultado = verificarRol(request, ['super_admin', 'administrador'])
    if resultado is not True:
        return resultado

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    filtros = {'flag': 'nuevo', 'estado': 'verificado'}

 
    if fecha_inicio and fecha_fin:
        filtros['fecha_verificacion__date__gte'] = fecha_inicio
        filtros['fecha_verificacion__date__lte'] = fecha_fin

    tramite = Tramite.objects.filter(**filtros)

    paginator = Paginator(tramite, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin
    }
    return render(request, 'tramite/verificado.html', context)


def observadosramite(request):
    resultado = verificarRol(request, ['super_admin', 'administrador'])
    if resultado is not True:
        return resultado
    
 
    tramite = Tramite.objects.filter(flag='nuevo', estado='observado')

 
    paginator = Paginator(tramite, 20)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  

   
    context = {'page_obj': page_obj}
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
            #afiliado = get_object_or_404(Afiliado, pk =  d["afiliado_id"])
            #ruta = get_object_or_404(Rutas, pk=d["ruta_nombre_mostrar"])
            vehiculo=Vehiculo.objects.create(marca= d["marca"].title(), 
                                
                                modelo = d["modelo"].title(),
                                 placa= d["placa"], 
                                 tipo_transporte =d["tipo_transporte"],
                                 chasis= d["chasis"],
                                 capacidad= d["capacidad"]
                                 
                                #tipo_vehiculo=d["tipo_servicio"]
                                 )
        

            DetalleTramite.objects.create(vehiculo= vehiculo , rutas=d["ruta_nombre_mostrar"] , afiliado= d["afiliado"].title(), tramite= tramite, tipo_tarjeta=d['tipoTarjeta'])

          

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
        ruta = request.POST.get('rutas') 
        afiliado = request.POST.get('afiliado')    
        #r = get_object_or_404(Rutas, pk= ruta)
        placa = request.POST.get('placa')
        tipo_transporte = request.POST.get('tipo_transporte')
        modelo = request.POST.get('modelo')
        marca = request.POST.get('marca')
        chasis = request.POST.get('chasis')
        tipo_tarjeta = request.POST.get('tipo_tarjeta')
        capacidad = request.POST.get('capacidad')
        
    
        tramite.vehiculo.placa = placa
        tramite.vehiculo.tipo_transporte= tipo_transporte
        tramite.vehiculo.modelo = modelo
        tramite.vehiculo.marca = marca
        tramite.vehiculo.chasis =chasis
        tramite.tipo_tarjeta= tipo_tarjeta
        tramite.vehiculo.capacidad = capacidad
        tramite.rutas= ruta
        tramite.afiliado = afiliado
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
            Rutas.objects.create(nombre=nombre.title())
            return JsonResponse({'estatus': 201})
        except Exception as e:
            return JsonResponse({'estatus': 500, 'mensaje': str(e)}, status=500)
def listarRuta(request):
    rutas = Rutas.objects.all()  
    rutas_data = list(rutas.values('id', 'nombre'))  
    return JsonResponse(rutas_data, safe=False)

def descargarDetalleCompleto(request, id):
    tramite = get_object_or_404(Tramite, pk=id)
    detalles = DetalleTramite.objects.filter(tramite=tramite)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="licencia_operacion.pdf"'
    response['X-Frame-Options'] = 'SAMEORIGIN'
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    margin = 40
    y = height - 40
    for detalle in detalles:
        if y < 200:
            p.showPage()
            y = height - 40

        qr_texto = (
            f"Placa: {capitalizar_palabras(detalle.vehiculo.placa)}\n"
            f"Trámite: {detalle.tramite.numero_tramite}\n"
            f"Operador: {capitalizar_palabras(str(detalle.afiliado))}\n"
            f"Modelo: {capitalizar_palabras(detalle.vehiculo.modelo)}\n"
            f"Marca: {capitalizar_palabras(detalle.vehiculo.marca)}\n"
            f"Chasis: {capitalizar_palabras(detalle.vehiculo.chasis)}\n"
            f"Capacidad: {capitalizar_palabras(str(detalle.vehiculo.capacidad))}\n"
            f"Rutas: {capitalizar_palabras(detalle.rutas)}\n"
            f"Válida del: {detalle.tramite.fecha_validezI} al {detalle.tramite.fecha_validezF}"
        )

        p.setFont("Helvetica-Bold", 10)
        p.drawString(margin, y, f"Nro. Trámite: {tramite.numero_tramite}")
        p.drawRightString(width - margin, y, f"Técnico : {capitalizar_palabras(tramite.usuario.username)}")
        y -= 15

        p.setFont("Helvetica", 9)
        p.drawString(margin, y, f"Empresa: {capitalizar_palabras(detalle.tramite.operador.nombre)}")
        y -= 15
        p.drawString(margin, y, f"Propietario: {capitalizar_palabras(str(detalle.afiliado)) if detalle.afiliado else ''}")
        y -= 15

        qr_code = qr.QrCodeWidget(qr_texto)
        qr_code.barWidth = 90
        qr_code.barHeight =90
        d = Drawing(90, 90)
        d.add(qr_code)
        renderPDF.draw(d, p, width - 150, y - 50)

        col1 = margin
        col2 = margin + 230

        p.drawString(col1, y, f"Placa: {capitalizar_palabras(detalle.vehiculo.placa)}")
        p.drawString(col2, y, f"Tipo Transporte: {capitalizar_palabras(detalle.vehiculo.tipo_transporte)}")
        y -= 12
        p.drawString(col1, y, f"Modelo: {capitalizar_palabras(detalle.vehiculo.modelo)}")
        p.drawString(col2, y, f"Marca: {capitalizar_palabras(detalle.vehiculo.marca)}")
        y -= 12
        p.drawString(col1, y, f"Nro. Registro: {str(detalle.vehiculo.pk)}")
        p.drawString(col2, y, f"Chasis : {capitalizar_palabras(detalle.vehiculo.chasis)}")
        y -= 12
        p.drawString(col2, y, f"Capacidad: {str(detalle.vehiculo.capacidad)}")
        y -= 12

        p.drawString(margin, y, f"Rutas Autorizadas:")
        y -= 12
        p.drawString(margin, y, capitalizar_palabras(detalle.rutas))
        y -= 12
        p.drawString(margin, y, f"Validez:")
        p.drawString(margin + 50, y, f"{detalle.tramite.fecha_validezI} a {detalle.tramite.fecha_validezF}")
        p.drawRightString(width - margin, y, f"Monto: {tramite.monto} Bs.")
        y -= 20

        p.setFont("Helvetica", 9)
        if tramite.fecha_creacion:
            p.drawString(margin, y, f"Fecha de creación: {tramite.fecha_creacion.strftime('%d/%m/%Y')}")
            p.drawRightString(width - margin, y, f"Hora: {tramite.fecha_creacion.strftime('%H:%M')}")
            y -= 12

        y -= 10
        p.setStrokeColor(colors.grey)
        p.line(margin, y, width - margin, y)
        y -= 15

    p.setFont("Helvetica", 8)
    p.drawRightString(width - margin, 30, f"Potosí - {datetime.now().strftime('%d/%m/%Y')}")

    p.save()
    return response

def generar_licencia_pdf(request, id):
    detalle = get_object_or_404(DetalleTramite, pk=id)
    qr_texto = (
        f"Placa: {capitalizar_palabras(detalle.vehiculo.placa)}\n"
        f"Trámite: {detalle.tramite.numero_tramite}\n"
        f"Operador: {capitalizar_palabras(str(detalle.afiliado))}\n"
        f"Modelo: {capitalizar_palabras(detalle.vehiculo.modelo)}\n"
        f"Marca: {capitalizar_palabras(detalle.vehiculo.marca)}\n"
        f"Chasis: {capitalizar_palabras(detalle.vehiculo.chasis)}\n"
        f"Capacidad: {capitalizar_palabras(str(detalle.vehiculo.capacidad))}\n"
        f"Rutas: {capitalizar_palabras(detalle.rutas)}\n"
        f"Válida del: {detalle.tramite.fecha_validezI} al {detalle.tramite.fecha_validezF}"
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="licencia_operacion.pdf"'
    response['X-Frame-Options'] = 'SAMEORIGIN'

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
    p.drawString(140, y, capitalizar_palabras(detalle.tramite.operador.federacion))
    y -= 18

   
    datos_col1 = [
        ("Operador:", capitalizar_palabras(str(detalle.afiliado))),
        ("Modelo:", capitalizar_palabras(detalle.vehiculo.modelo)),
        ("Registro:", str(detalle.tramite.numero_tramite)),
    ]
    datos_col2 = [
        ("Capacidad:", capitalizar_palabras(str(detalle.vehiculo.capacidad))),
        ("Chasis:", capitalizar_palabras(detalle.vehiculo.chasis)),
        ("Marca:", capitalizar_palabras(detalle.vehiculo.marca)),
    ]

    x1 = 50
    x2 = width / 2 + 10
    for i in range(3):
        p.setFont("Helvetica-Bold", 8)
        p.drawString(x1, y, datos_col1[i][0])
        p.setFont("Helvetica", 8)
        p.drawString(x1 + 90, y, datos_col1[i][1])

        p.setFont("Helvetica-Bold", 8)
        p.drawString(x2, y, datos_col2[i][0])
        p.setFont("Helvetica", 8)
        p.drawString(x2 + 80, y, datos_col2[i][1])
        y -= 14

    # Placa centrada capitalizada
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.black)
    p.drawCentredString(width / 2, y - 10, capitalizar_palabras(detalle.vehiculo.placa))
    y -= 25

    p.setStrokeColor(colors.black)
    p.line(40, y, width - 40, y)
    y -= 12

    # Rutas
    p.setFont("Helvetica-Bold", 8)
    p.drawString(50, y, "Rutas Autorizadas:")
    p.setFont("Helvetica", 8)
    y -= 12
    p.drawString(70, y, capitalizar_palabras(detalle.rutas))
    y -= 18

    # Validez
    p.setFont("Helvetica-Bold", 8)
    p.drawString(50, y, "Licencia válida de:")
    p.setFont("Helvetica", 8)
    p.drawString(140, y, f"{detalle.tramite.fecha_validezI} al {detalle.tramite.fecha_validezF}")
    y -= 30

    # Código QR
    qr_code = qr.QrCodeWidget(qr_texto)
    qr_code.barWidth = 90
    qr_code.barHeight = 90
    d = Drawing(100, 100)
    d.add(qr_code)

    renderPDF.draw(d, p, width - 150, 120)

    # Firmas
    p.setFont("Helvetica-Bold", 8)
    p.drawString(50, 60, "Abog. Guido Soux Velasquez")
    p.setFont("Helvetica", 7)
    p.drawString(50, 50, "SECRETARIO DEPARTAMENTAL")
    p.drawString(50, 40, "DE JURÍDICA")

    p.setFont("Helvetica-Bold", 8)
    p.drawRightString(width - 50, 60, "Oscar Mendoza Mamani")
    p.setFont("Helvetica", 7)
    p.drawRightString(width - 50, 50, "SECRETARIO DEPARTAMENTAL")
    p.drawRightString(width - 50, 40, "DE COORDINACIÓN GENERAL")

    p.showPage()
    p.save()
    return response

def capitalizar_palabras(texto):
    if not texto:
        return ""
    if not isinstance(texto, str):
        texto = str(texto)
    return " ".join(palabra.capitalize() for palabra in texto.split())