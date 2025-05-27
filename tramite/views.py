import os
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.template.loader import get_template
from django.utils import timezone

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

from xhtml2pdf import pisa

from io import BytesIO
import qrcode
import base64
import json
from datetime import datetime

from federacion.models import Federacion
from log.views import registrar_log
from operador.models import Operador
from tramite.models import Tramite, Rutas
from vehiculo.models import Vehiculo
from usuarios.models import Usuario
from afiliados.models import Afiliado
from .models import DetalleTramite
from utils.context_processors import verificarRol
from django.contrib.auth.decorators import login_required

@login_required
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

            t= Tramite.objects.create(
                tipo_tramite=tipo,
                fecha_validezI=fecha_validezI,
                fecha_validezF=fecha_validezF,
                gestion=gestion,
               operador=operador,
                usuario=tecnico,
                numero_fojas= fojas,
                fecha_creacion=timezone.now()
            )
            registrar_log(request,'tramite',request.user.username, f'se registro un tramite con el numero {t.numero_tramite}')

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


@login_required
def verTramite(request, id):
    resultado = verificarRol(request, ['super_admin','administrador','tecnico'])
    if resultado is not True:
        return resultado
    tramite = get_object_or_404(Tramite, pk=id)

    if request.method =='POST':
            estado = request.POST.get('estado')
            detalle = request.POST.get('detalle')
            if estado == 'verificado':
                tramite.estado = estado
                tramite.fecha_verificacion = timezone.now()
            if estado == 'observado':
                tramite.estado = estado
                tramite.observaciones = detalle
                tramite.fecha_observacion = timezone.now()
            tramite.save()
            registrar_log(request,'tramite',request.user.username, f'El numero de tramite {tramite.numero_tramite} cambio de estado  {estado}')
            return redirect(reverse('listarTramite'))
    else:
       
        context={'id':id,'tramite':tramite}

        return render(request,'tramite/verTramite.html', context)

@login_required
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
@login_required
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

@login_required
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

@login_required
def detalleTramite (request, id):
    tramite = get_object_or_404(Tramite, pk=id)
    detalle = DetalleTramite.objects.filter(tramite= tramite)
    context  = {
        'tramite':tramite,
        'detalle':detalle
    }
    return render(request,'tramite/detalleTramite.html', context)
@login_required
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
            
        

            DetalleTramite.objects.create(vehiculo= vehiculo , costo_tarjeta = d["costo_tarjeta"], rutas=d["ruta_nombre_mostrar"] , afiliado= d["afiliado"].title(), tramite= tramite, tipo_tarjeta=d['tipoTarjeta'])
            registrar_log(request,'vehiculo',request.user.username, f'se registro un vehiculo con la placa  {d["placa"]}')
          

        print('registrado')
        
        return JsonResponse({"status": "success"}, status=201)
    afiliado = Afiliado.objects.filter(federacion = tramite.operador.federacion)
    context  = {
        'tramite':tramite,
        'afiliados':afiliado
    }
    return render(request,'tramite/tarjeta.html', context)
@login_required
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
        costo_tarjeta = request.POST.get('costo_tarjeta')
        print('costo_tarjeta',costo_tarjeta)
    
        tramite.vehiculo.placa = placa
        tramite.vehiculo.tipo_transporte= tipo_transporte
        tramite.vehiculo.modelo = modelo
        tramite.vehiculo.marca = marca
        tramite.costo_tarjeta=costo_tarjeta
        tramite.vehiculo.chasis =chasis
        tramite.tipo_tarjeta= tipo_tarjeta
        tramite.vehiculo.capacidad = capacidad
        tramite.rutas= ruta
        tramite.afiliado = afiliado
        tramite.vehiculo.save()
        tramite.save()
        registrar_log(request,'tramite',request.user.username, f'se edito el tramite con el numero  {tramite.tramite.numero_tramite}')
        return redirect(reverse('verificadoTramite'))

    context  = {
        'tramite':tramite
    }
    return  render(request,'tramite/editarTramite.html',context)
@login_required
def aprobarTramite(request, id):
    tramite= get_object_or_404(Tramite, pk=id)
    tramite.estado ='aprobado'
    
    tramite.save()
    
    return redirect(reverse('listarTramite'))
@login_required
def anularTramite(request, id):
    tramite= get_object_or_404(Tramite, pk=id)
    tramite.estado ='anulado'
    tramite.save()
    return redirect(reverse('listarTramite'))
@login_required
def verificarPago(request, id):
    tramite = get_object_or_404(Tramite, pk= id)
    if request.method =='POST':
        
        numeroComprobante = request.POST.get('numeroComprobante')
        fechaPago = request.POST.get('fechaPago')
        monto = request.POST.get('monto')
        banco = request.POST.get('banco')
        print(banco)
        tramite.numero_comprobante= numeroComprobante
        tramite.fecha_pago= fechaPago
        tramite.monto = monto
        tramite.banco= banco.upper()
        tramite.verificarPago= True
        tramite.save()
        registrar_log(request,'tramite',request.user.username, f'Realizo el pago de tramite   {tramite.numero_tramite}')
        return redirect(reverse('verificadoTramite'))
    return render(request, 'tramite/verificarPago.html', {'id':tramite.id})

@login_required
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
@login_required
def listarRuta(request):
    rutas = Rutas.objects.all()  
    rutas_data = list(rutas.values('id', 'nombre'))  
    return JsonResponse(rutas_data, safe=False)

@login_required
def tramitesVigentes(request):
    today = datetime.today() 

    filtros = {
        'flag': 'nuevo',
        'estado': 'verificado',
        'fecha_validezI__lte': today,  
        'fecha_validezF__gte': today,
    }

    tramites = Tramite.objects.filter(**filtros)

    paginator = Paginator(tramites, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }

    return render(request, 'tramite/tramitesVigentes.html', context)

def dibujar_encabezado(p, width, height, margin):
    y_encabezado = height - 50
    ruta_logo = os.path.join("static", "imagen", "log.png")
    ancho_logo = 50
    alto_logo = 50
    x_logo = margin
    y_logo = height - alto_logo - 35
    p.drawImage(ruta_logo, x_logo, y_logo, width=ancho_logo, height=alto_logo, mask='log')
    p.setFont("Helvetica-Bold", 11)
    p.drawCentredString(width / 2, y_encabezado, "GOBIERNO AUTÓNOMO DEPARTAMENTAL DE POTOSÍ")
    y_encabezado -= 15
    p.setFont("Helvetica", 10)
    p.drawCentredString(width / 2, y_encabezado, "UNIDAD DE REGISTRO Y REGULACIÓN DE TRANSPORTE")
    y_encabezado -= 15
    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(width / 2, y_encabezado, "FORMULARIO DE VERIFICACIÓN DE DATOS - TARJETA INTERPROVINCIAL")
    return y_encabezado - 2

@login_required
def descargarDetalleCompleto(request, id):
    tramite = get_object_or_404(Tramite, pk=id)
    detalles = DetalleTramite.objects.filter(tramite=tramite)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="licencia_operacion.pdf"'
    response['X-Frame-Options'] = 'SAMEORIGIN'
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    margin = 70
    y = height - 100
    y = dibujar_encabezado(p, width, height, margin)
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
        y -= 30

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
        qr_code.barWidth = 120
        qr_code.barHeight = 120
        d = Drawing(120, 120)
        d.add(qr_code)
        renderPDF.draw(d, p, width - 150, y - 70)

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
        p.drawRightString(width - margin, y, f"Monto: {detalle.costo_tarjeta} Bs.")
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

    # Fecha al pie de la última página de contenido
    p.setFont("Helvetica", 8)
    p.drawRightString(width - margin, 30, f"Potosí - {datetime.now().strftime('%d/%m/%Y')}")

    # NUEVA HOJA PARA EL INSTRUCTIVO
   
    width, height = letter
    footer_y = 100

    p.setFont("Helvetica-Bold", 9)
    p.drawString(margin, footer_y + 90, "Instructivo:")
    if y < 200:
        p.showPage()
        y  = height - 40
    p.setFont("Helvetica", 8)
    p.drawString(margin + 10, footer_y + 78, "a) Lea detalladamente los datos de cada uno de los vehículos en el presente formulario.")
    p.drawString(margin + 10, footer_y + 67, "b) Si encuentra algún error, resaltarlo y devolverlo a Unidad Registro y Regulación de Transporte")
    p.drawString(margin + 25, footer_y + 56, "para su corrección sin firmar.")
    p.drawString(margin + 10, footer_y + 45, "c) Si todos los datos están correctos, firmar el formulario y proceder a realizar el depósito")
    p.drawString(margin + 25, footer_y + 34, f"correspondiente en la cuenta N: 1-6024553 del BANCO UNION por el total de las tarjetas, luego")
    p.drawString(margin + 25, footer_y + 23, "entregar fotocopia del presente formulario y del comprobante de depósito a Tesorería de la")
    p.drawString(margin + 25, footer_y + 12, "Gobernación.")
    
    p.setFont("Helvetica-Bold", 8)
    p.drawString(margin, footer_y - 8, "JURO LA EXACTITUD DE LOS DATOS DEL PRESENTE FORMULARIO")
    p.drawString(width - 230, footer_y - 8, "ACLARACIÓN DE LA FIRMA")
    footer_y = 80
    p.setFont("Helvetica", 8)
    p.line(margin, footer_y - 20, margin + 150, footer_y - 20)
    p.drawString(margin + 40, footer_y - 32, "Firma Rep. legal")
    p.drawString(width - 210, footer_y - 20, "Nombre: __________________________")
    p.drawString(width - 210, footer_y - 38, "C.I.: __________________________")

    p.save()
    return response



@login_required
def generar_licencia_pdf(request, id):
    detalle = get_object_or_404(DetalleTramite, pk=id)

    # Texto para el QR
    qr_texto = (
        f"PLACA: {str(detalle.vehiculo.placa).upper()}\n"
        f"TRÁMITE: {str(detalle.tramite.numero_tramite).upper()}\n"
        f"OPERADOR: {str(detalle.afiliado).upper()}\n"
        f"MODELO: {str(detalle.vehiculo.modelo).upper()}\n"
        f"MARCA: {str(detalle.vehiculo.marca).upper()}\n"
        f"CHASIS: {str(detalle.vehiculo.chasis).upper()}\n"
        f"CAPACIDAD: {str(detalle.vehiculo.capacidad).upper()}\n"
        f"RUTAS: {str(detalle.rutas).upper()}\n"
        f"VÁLIDA DEL: {detalle.tramite.fecha_validezI} AL {detalle.tramite.fecha_validezF}"
    )

    # Generar QR
    qr_img = qrcode.make(qr_texto)
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    # HTML con QR embebido
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                font-size: 12px;
                margin: 0;
                padding: 0;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                table-layout: fixed;
                 
            }}
            td, th {{
                border: 1px solid #000;
                padding: 6px;
                vertical-align: top;
            }}
            .titulo {{
                text-align: center;
                font-weight: bold;
                font-size: 14px;
                padding: 10px;
             
            }}
            .operador {{
                font-weight: bold;
                border: 1px solid black;
                padding: 6px;
            }}
            .qr {{
                text-align: center;
                
            }}
            .no-border {{
             
            }}
        </style>
    </head>
    <body>
        <br>
        <br><br><br><br><br><br><br>
       <table>
    <tr>
        <td colspan="4" class="titulo">
            LICENCIA DE OPERACIÓN PARA EL TRANSPORTE<br>
            AUTOMOTOR INTERPROVINCIAL - ATL
        </td>
       <td rowspan="6" class="qr" style="vertical-align: middle;">
    <img src="data:image/png;base64,{qr_base64}" width="120"><br><br>
    <div style="font-size: 20px; font-weight: bold;">{str(detalle.vehiculo.placa).upper()}</div><br>
    FECHA DE VALIDEZ<br>
    {detalle.tramite.fecha_validezI} : {detalle.tramite.fecha_validezF}
</td>
    </tr>
    <tr>
        <td colspan="4" class="operador">
            OPERADOR: {detalle.tramite.operador.nombre.upper()} AFILIADA A LA FEDERACIÓN {detalle.tramite.operador.federacion.nombre.upper()}
        </td>
    </tr>
    <tr>
        <td colspan="3"><strong>AFILIADO</strong><br>{detalle.afiliado.upper()}</td>
        <td><strong>MODELO</strong><br>{detalle.vehiculo.modelo.upper()}</td>
       
    </tr>
    <tr>
        <td><strong>CATEGORÍA</strong><br>PASAJEROS</td>
        <td><strong>MARCA</strong><br>{detalle.vehiculo.marca.upper()}</td>
        <td><strong>CAPACIDAD</strong><br>{detalle.vehiculo.capacidad}</td>
        <td colspan="1"><strong>REGISTRO</strong><br>{detalle.tramite.pk}</td>
    </tr>
    <tr>
        <td colspan="4"><strong>RUTAS</strong><br>{detalle.rutas.upper()}</td>
    </tr>
    <tr>
        <td colspan="4" class="no-border">&nbsp;</td> <!-- Espacio extra para altura -->
    </tr>
    <tr>
    <td colspan="5" style="border: none; padding-top: 40px;">
        <table style="width: 100%; border: none;">
            <tr>
                <td style="width: 50%; text-align: center; border: none;">
                    ...............................................<br>
                    <strong>Abog. Guido Velazquez</strong><br>
                      <strong>SECRETARIO DEPARTAMENTE DE JUDIRICA</strong>
                </td>
                <td style="width: 50%; text-align: center; border: none;">
                    ...............................................<br>
                    <strong>Oscar mendoza Mamani</strong><br>
                    <strong>SECRETARIO DEPARTARTAMENTAL DE COORDINACION GENERAL</strong>
                </td>
            </tr>
        </table>
    </td>
</tr>

</table>

    </body>
    </html>
    """

    # Generar el PDF
    resultado = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), resultado)

    if not pdf.err:
        response = HttpResponse(resultado.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="licencia.pdf"'
        response['X-Frame-Options'] = 'SAMEORIGIN'
        return response
    else:
        return HttpResponse("Error al generar el PDF", status=500)

def capitalizar_palabras(texto):
    if not texto:
        return ""
    if not isinstance(texto, str):
        texto = str(texto)
    return " ".join(palabra.capitalize() for palabra in texto.split())