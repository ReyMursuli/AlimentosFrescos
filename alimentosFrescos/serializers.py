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
    cliente_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'cliente_id', 'cantidad', 'precio', 'estado', 'fecha_creacion', 'productos']

    def create(self, validated_data):
        cliente_id = validated_data.pop('cliente_id')
        validated_data['cliente_id'] = cliente_id
        return super().create(validated_data)

class CompraSerializer(serializers.ModelSerializer):
    proveedor = ProveedorSerializer(read_only=True)
    producto = ProductoSerializer(read_only=True)
    proveedor_id = serializers.IntegerField(write_only=True)


    class Meta:
        model = Compra
        fields = ['id', 'proveedor', 'proveedor_id', 'producto', 'cantidad', 'precio', 'fecha_creacion']

    def create(self, validated_data):
        proveedor_id = validated_data.pop('proveedor_id')
        validated_data['proveedor_id'] = proveedor_id
        return super().create(validated_data)