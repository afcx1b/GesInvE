from django.urls import path
from .views import (
    ClienteListView, ClienteCreateView, ClienteUpdateView, ClienteDeleteView,
    VentaListView, VentaCreateView, VentaUpdateView, VentaDeleteView,
    PrecioVentaListView, PrecioVentaCreateView, PrecioVentaUpdateView, PrecioVentaDeleteView,
    ComisionVendedorListView, ComisionVendedorCreateView, ComisionVendedorUpdateView, ComisionVendedorDeleteView
)

app_name = 'sales'

urlpatterns = [
    # URLs para Clientes
    path('clientes/', ClienteListView.as_view(), name='cliente_list'),
    path('clientes/nuevo/', ClienteCreateView.as_view(), name='cliente_create'),
    path('clientes/editar/<int:pk>/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('clientes/eliminar/<int:pk>/', ClienteDeleteView.as_view(), name='cliente_delete'),
    
    # URLs para Ventas
    path('ventas/', VentaListView.as_view(), name='sale_list'),
    path('ventas/nueva/', VentaCreateView.as_view(), name='venta_create'),
    path('ventas/editar/<int:pk>/', VentaUpdateView.as_view(), name='venta_update'),
    path('ventas/eliminar/<int:pk>/', VentaDeleteView.as_view(), name='venta_delete'),
    
    # URLs para Precios de Venta
    path('precios/', PrecioVentaListView.as_view(), name='precioventa_list'),
    path('precios/nuevo/', PrecioVentaCreateView.as_view(), name='precioventa_create'),
    path('precios/editar/<int:pk>/', PrecioVentaUpdateView.as_view(), name='precioventa_update'),
    path('precios/eliminar/<int:pk>/', PrecioVentaDeleteView.as_view(), name='precioventa_delete'),
    
    # URLs para Comisiones de Vendedores
    path('comisiones/', ComisionVendedorListView.as_view(), name='comision_list'),
    path('comisiones/nueva/', ComisionVendedorCreateView.as_view(), name='comision_create'),    
    path('comisiones/editar/<int:pk>/', ComisionVendedorUpdateView.as_view(), name='comision_update'),
    path('comisiones/eliminar/<int:pk>/', ComisionVendedorDeleteView.as_view(), name='comision_delete'),
]
