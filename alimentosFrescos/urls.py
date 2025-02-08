from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsuarioViewSet, ProveedorViewSet,
    ClienteViewSet, PedidoViewSet, ProductoViewSet, CompraViewSet,
    top_proveedores, top_clientes, productos_mas_vendidos,
    compras_por_dia, compras_por_mes, pedidos_cliente,
    exportar_pedidos_pdf
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'compras', CompraViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('top-proveedores/', top_proveedores, name='top-proveedores'),
    path('top-clientes/', top_clientes, name='top-clientes'),
    path('productos-mas-vendidos/', productos_mas_vendidos, name='productos-mas-vendidos'),
    path('compras-por-dia/', compras_por_dia, name='compras-por-dia'),
    path('compras-por-mes/', compras_por_mes, name='compras-por-mes'),
    path('pedidos-cliente/', pedidos_cliente, name='pedidos-cliente'),
    path('exportar-pedidos-pdf/', exportar_pedidos_pdf, name='exportar-pedidos-pdf'),
]
