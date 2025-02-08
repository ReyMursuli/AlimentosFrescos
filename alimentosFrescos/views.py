from django.shortcuts import render
from rest_framework import viewsets
from .models import Usuario, Proveedor, Cliente, Pedido, Producto, Compra
from .serializers import (
    UsuarioSerializer, ProveedorSerializer, ClienteSerializer, PedidoSerializer, ProductoSerializer, CompraSerializer
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Count, Sum
from rest_framework import filters
from django_filters import rest_framework as django_filters
from datetime import datetime
from django.db.models.functions import TruncMonth
from django.db import models
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

# Create your views here.

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de Usuario
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    # permission_classes = [IsAuthenticated]

class ProveedorViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de Proveedor
    """
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de Cliente
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def perform_create(self, serializer):
        # Aquí puedes agregar lógica antes de guardar
        serializer.save()

class ProductoFilter(django_filters.FilterSet):
    tipo = django_filters.CharFilter(lookup_expr='icontains')
    precio_min = django_filters.NumberFilter(field_name='precio_costo', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio_costo', lookup_expr='lte')
    
    class Meta:
        model = Producto
        fields = ['tipo', 'precio_min', 'precio_max']

class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de Producto
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductoFilter
    search_fields = ['nombre', 'tipo']

class PedidoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de Pedido
    """
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def perform_create(self, serializer):
        
        serializer.save()

class CompraViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de Compra
    """
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

    def perform_create(self, serializer):
        
        serializer.save()

@api_view(['GET'])
def top_proveedores(request):
    proveedores = Proveedor.objects.annotate(
        total_ventas=Count('compras'),
        total_cantidad=Sum('compras__cant')
    ).order_by('-total_ventas')[:10]
    
    resultado = [{
        'id': p.id,
        'nombre': p.nombre,
        'total_ventas': p.total_ventas,
        'total_cantidad': p.total_cantidad or 0
    } for p in proveedores]
    
    return Response(resultado)

@api_view(['GET'])
def top_clientes(request):
    clientes = Cliente.objects.annotate(
        total_compras=Count('pedidos'),
        total_gastado=Sum('pedidos__precio')
    ).order_by('-total_compras')[:10]
    
    resultado = [{
        'id': c.id,
        'nombre': c.nombre,
        'total_compras': c.total_compras,
        'total_gastado': float(c.total_gastado or 0)
    } for c in clientes]
    
    return Response(resultado)

@api_view(['GET'])
def productos_mas_vendidos(request):
    productos = Producto.objects.annotate(
        total_pedidos=Count('pedidos'),
        total_vendido=Sum('pedidos__cantidad')
    ).order_by('-total_pedidos')[:10]
    
    resultado = [{
        'id': p.id,
        'nombre': p.nombre,
        'tipo': p.tipo,
        'precio': float(p.precio_costo),
        'total_pedidos': p.total_pedidos,
        'cantidad_total_vendida': p.total_vendido or 0
    } for p in productos]
    
    return Response(resultado)

@api_view(['GET'])
def compras_por_dia(request):
    fecha = request.query_params.get('fecha', datetime.now().date())
    
    compras = Compra.objects.filter(fecha=fecha).select_related('proveedor', 'producto')
    
    resultado = [{
        'id': c.id,
        'proveedor': c.proveedor.nombre,
        'producto': c.producto.nombre,
        'cantidad': c.cant,
        'precio': float(c.precio),
        'fecha': c.fecha
    } for c in compras]
    
    total_dia = sum(c.precio * c.cant for c in compras)
    
    return Response({
        'fecha': fecha,
        'total_compras': len(resultado),
        'total_gastado': float(total_dia),
        'compras': resultado
    })

@api_view(['GET'])
def compras_por_mes(request):
    compras = Compra.objects.annotate(
        mes=TruncMonth('fecha')
    ).values('mes').annotate(
        total_compras=Count('id'),
        total_gastado=Sum(models.F('precio') * models.F('cant'))
    ).order_by('-mes')
    
    resultado = [{
        'mes': c['mes'].strftime('%Y-%m'),
        'total_compras': c['total_compras'],
        'total_gastado': float(c['total_gastado'] or 0)
    } for c in compras]
    
    return Response(resultado)

@api_view(['GET'])
def pedidos_cliente(request):
    cliente_id = request.query_params.get('cliente_id')
    
    if not cliente_id:
        return Response({
            'error': 'Debe proporcionar un cliente_id'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        cliente = Cliente.objects.get(id=cliente_id)
        pedidos = Pedido.objects.filter(cliente=cliente).select_related('cliente')
        
        resultado = {
            'cliente': {
                'id': cliente.id,
                'nombre': cliente.nombre,
                'tipo': cliente.tipo
            },
            'total_pedidos': pedidos.count(),
            'total_gastado': float(pedidos.aggregate(total=Sum('precio'))['total'] or 0),
            'pedidos': [{
                'id': p.id,
                'fecha': p.fecha_creacion,
                'cantidad': p.cantidad,
                'precio': float(p.precio),
                'estado': p.estado,
                'productos': [
                    {
                        'id': prod.id,
                        'nombre': prod.nombre,
                        'tipo': prod.tipo,
                        'precio': float(prod.precio_costo)
                    } for prod in p.productos.all()
                ]
            } for p in pedidos]
        }
        
        return Response(resultado)
        
    except Cliente.DoesNotExist:
        return Response({
            'error': 'Cliente no encontrado'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def exportar_pedidos_pdf(request):
    # Crear el response con tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pedidos.pdf"'
    
    # Crear el documento PDF
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    
    # Obtener todos los pedidos
    pedidos = Pedido.objects.select_related('cliente').all()
    
    # Preparar los datos para la tabla
    data = [['ID', 'Cliente', 'Fecha', 'Cantidad', 'Precio', 'Estado']]
    for pedido in pedidos:
        data.append([
            str(pedido.id),
            pedido.cliente.nombre,
            pedido.fecha_creacion.strftime('%Y-%m-%d'),
            str(pedido.cantidad),
            f"${pedido.precio}",
            pedido.estado
        ])
    
    # Crear la tabla
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    return response


