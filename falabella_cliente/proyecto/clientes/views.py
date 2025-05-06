from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Cliente, Compra
from .serializers import ClienteSerializer
import pandas as pd
from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import render, redirect



def home(request):
    return render(request, 'clientes/home.html')


def ping(request):
    return JsonResponse({'message': 'pong'})


@api_view(['GET'])
def buscar_cliente(request):
    tipo_documento = request.GET.get('tipo_documento')
    numero_documento = request.GET.get('numero_documento')

    if not tipo_documento or not numero_documento:
        return Response({"error": "Debe proporcionar 'tipo_documento' y 'numero_documento'"}, status=400)

    try:
        cliente = Cliente.objects.get(
            tipo_documento__id=tipo_documento,
            numero_documento=numero_documento
        )
        serializer = ClienteSerializer(cliente)

        # Traer las compras también
        compras = Compra.objects.filter(cliente=cliente).values('descripcion', 'monto', 'fecha')
        compras_list = list(compras)

        return Response({
            "cliente": serializer.data,
            "compras": compras_list
        })

    except Cliente.DoesNotExist:
        return Response({"error": "Cliente no encontrado"}, status=404)


@api_view(['GET'])
def exportar_cliente_excel(request):
    tipo_documento = request.GET.get('tipo_documento')
    numero_documento = request.GET.get('numero_documento')

    if not tipo_documento or not numero_documento:
        return Response({"error": "Debe proporcionar 'tipo_documento' y 'numero_documento'"}, status=400)

    try:
        cliente = Cliente.objects.get(
            tipo_documento__id=tipo_documento,
            numero_documento=numero_documento
        )
        compras = Compra.objects.filter(cliente=cliente)

        if not compras.exists():
            data = [{
                "Nombre": cliente.nombre,
                "Apellido": cliente.apellido,
                "Correo": cliente.correo,
                "Teléfono": cliente.telefono,
                "Fecha de Compra": "No tiene compras",
                "Monto": "No tiene compras",
                "Descripción": "No tiene compras"
            }]
        else:
            data = [{
                "Nombre": cliente.nombre,
                "Apellido": cliente.apellido,
                "Correo": cliente.correo,
                "Teléfono": cliente.telefono,
                "Fecha de Compra": c.fecha.strftime('%Y-%m-%d'),
                "Monto": c.monto,
                "Descripción": c.descripcion
            } for c in compras]

        df = pd.DataFrame(data)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=cliente_{numero_documento}.xlsx'
        df.to_excel(response, index=False)

        return response

    except Cliente.DoesNotExist:
        return Response({"error": "Cliente no encontrado"}, status=404)


@api_view(['GET'])
def reporte_fidelizacion(request):
    # Calcula la fecha hace 30 días
    ultimo_mes = datetime.today() - timedelta(days=30)

    # Obtiene todos los clientes
    clientes = Cliente.objects.all()
    data = []

    for cliente in clientes:
        # Filtra las compras de ese cliente en el último mes
        compras_mes = Compra.objects.filter(cliente=cliente, fecha__gte=ultimo_mes)

        # Calcula el total de esas compras
        total = sum([c.monto for c in compras_mes])

        # Si el total supera los 5 millones, lo agregamos al reporte
        if total >= 5000000:
            data.append({
                "Nombre": cliente.nombre,
                "Apellido": cliente.apellido,
                "Correo": cliente.correo,
                "Teléfono": cliente.telefono,
                "Total Compras Último Mes (COP)": total
            })

    # Si no hay clientes que cumplan el criterio, devolvemos un mensaje
    if not data:
        return Response({"mensaje": "No hay clientes que superen los 5 millones en compras este mes."})

    # Creamos el DataFrame con pandas
    df = pd.DataFrame(data)

    # Preparamos la respuesta como archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=reporte_fidelizacion.xlsx'
    df.to_excel(response, index=False)

    return response

@api_view(['GET'])
def consultar_clientes_compras(request):
    clientes = Cliente.objects.all()
    data = []

    for cliente in clientes:
        compras = Compra.objects.filter(cliente=cliente)

        for compra in compras:
            data.append({
                "nombre": cliente.nombre,
                "apellido": cliente.apellido,
                "correo": cliente.correo,
                "telefono": cliente.telefono,
                "tipo_documento": cliente.tipo_documento.nombre,  # Tipo de documento
                "numero_documento": cliente.numero_documento,     # Número de documento
                "fecha": compra.fecha.strftime("%Y-%m-%d"),
                "descripcion": compra.descripcion,
                "monto": compra.monto
            })

    return Response(data)

