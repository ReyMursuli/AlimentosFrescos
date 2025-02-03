from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200)
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    def __str__(self):
        return f"Usuario: {self.nombre} - Tel: {self.telefono} - Dir: {self.direccion}"


class Proveedor(Usuario):
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
    def __str__(self):
        return f"Proveedor: {self.nombre} - Tel: {self.telefono}"



class Cliente(Usuario):
    usuario = models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    ci = models.CharField(max_length=20)
    def __str__(self):
        return f"Cliente: {self.nombre} - Tipo: {self.tipo} - CI: {self.ci}"
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

class Pedido(models.Model): #los pedidos son las coompras realizadas por un cliente 
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido de {self.cliente.nombre} - Estado: {self.estado} - Fecha: {self.fecha_creacion}"

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    unidad_medida = models.CharField(max_length=50)
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2)
    pedidos = models.ManyToManyField(Pedido, related_name='productos')

    def __str__(self):
        return f"Producto: {self.nombre} - Tipo: {self.tipo} - Precio: ${self.precio_costo}"

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

class Compra(models.Model):  #Una compra es lo que realiza alimentos frescos para la venta 
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name="compras")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="compras")
    fecha = models.DateField()
    cant = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Compra de {self.producto.nombre} - Proveedor: {self.proveedor.nombre} - Cantidad: {self.cant}"

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"

        