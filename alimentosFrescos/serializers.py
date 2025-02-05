from rest_framework import serializers
from .models import Usuario, Proveedor, Cliente, Pedido, Producto, Compra

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'  #preguntar por password
        

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    productos = ProductoSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = '__all__'

class CompraSerializer(serializers.ModelSerializer):
    proveedor = ProveedorSerializer(read_only=True)
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = Compra
        fields = '__all__'