from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsuarioViewSet, ProveedorViewSet,
    ClienteViewSet, PedidoViewSet, ProductoViewSet, CompraViewSet
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
]
