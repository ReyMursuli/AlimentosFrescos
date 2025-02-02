from rest_framework import serializers
from .models import Usuario, Proveedor, Administrador, Cliente, Pedido, Producto, Compra

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'usuario', 'roll', 'password', 'nombre', 'telefono', 'direccion']

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ['id', 'usuario', 'roll', 'password', 'nombre', 'telefono', 'direccion']

class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = ['id', 'usuario', 'roll', 'password', 'nombre', 'telefono', 'direccion']

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'usuario', 'roll', 'password', 'nombre', 'telefono', 'direccion', 'tipo', 'ci']

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'tipo', 'unidad_medida', 'precio_costo', 'pedidos']

class PedidoSerializer(serializers.ModelSerializer):
    productos = ProductoSerializer(many=True, read_only=True)
    cliente = ClienteSerializer(read_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'cantidad', 'precio', 'estado', 'fecha_creacion', 'productos']

class CompraSerializer(serializers.ModelSerializer):
    proveedor = ProveedorSerializer(read_only=True)
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = Compra
        fields = ['id', 'proveedor', 'producto', 'fecha', 'cant', 'precio']