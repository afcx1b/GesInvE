from django.urls import path
from . import views

app_name = 'buy'


urlpatterns = [
    path('proveedores/', views.lista_proveedores, name='lista_proveedores'),
    path('proveedores/agregar/', views.agregar_proveedor, name='agregar_proveedor'),
    path('', views.lista_compras, name='lista_compras'),
    path('compras/nueva/', views.crear_compra, name='crear_compra'),
    path('compras/<int:compra_id>/', views.detalle_compra, name='detalle_compra'),
]
