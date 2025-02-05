from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Usuario, Proveedor, Cliente, Pedido, Producto, Compra
from .serializers import (
    UsuarioSerializer, ProveedorSerializer, ClienteSerializer, PedidoSerializer, ProductoSerializer, CompraSerializer
)

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

class ProductoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de Producto
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class PedidoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de Pedido
    """
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer

    def perform_create(self, serializer):
        # Aquí puedes agregar lógica antes de guardar el pedido
        serializer.save()

class CompraViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operaciones CRUD de Compra
    """
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

    def perform_create(self, serializer):
        # Aquí puedes agregar lógica antes de guardar la compra
        serializer.save()
