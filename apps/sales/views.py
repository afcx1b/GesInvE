from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Cliente, Sale, SaleProduct, PrecioVenta, ComisionVendedor
from .forms import ClienteForm, VentaForm, SaleProductForm, PrecioVentaForm, ComisionVendedorForm
from apps.kardex.models import Kardex
from apps.inventory.models import Inventario
from apps.kardex.models import Precio

# Vista para listar clientes
class ClienteListView(ListView):
    model = Cliente
    template_name = 'ventas/cliente_list.html'
    context_object_name = 'clientes'

# Vista para crear un cliente
class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'ventas/cliente_form.html'
    success_url = reverse_lazy('cliente_list')

# Vista para actualizar un cliente
class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'ventas/cliente_form.html'
    success_url = reverse_lazy('cliente_list')

# Vista para eliminar un cliente
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'ventas/cliente_confirm_delete.html'
    success_url = reverse_lazy('cliente_list')





# Vista para listar ventas
class VentaListView(ListView):
    model = Sale
    template_name = 'ventas/venta_list.html'
    context_object_name = 'ventas'

class VentaCreateView(CreateView):
    model = Sale
    form_class = VentaForm
    template_name = 'ventas/venta_form.html'
    success_url = reverse_lazy('venta_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        venta = self.object

        # Registrar en Kardex
        for detalle in venta.detalles.all():
            Kardex.objects.create(
                articulo=detalle.articulo,
                cantidad=detalle.cantidad,
                tipo_movimiento='salida',
                fecha=venta.fecha,
                costo_unitario=detalle.articulo.costo,
                precio_venta=detalle.precio
            )

            # Registrar en Inventario
            inventario, created = Inventario.objects.get_or_create(producto=detalle.articulo)
            inventario.cantidad -= detalle.cantidad
            inventario.save()

            # Registrar en Precio
            Precio.objects.create(
                producto=detalle.articulo,
                precio=detalle.precio,
                fecha=venta.fecha
            )

        return response

# Vista para actualizar una venta
class VentaUpdateView(UpdateView):
    model = Sale
    form_class = VentaForm
    template_name = 'ventas/venta_form.html'
    success_url = reverse_lazy('venta_list')

# Vista para eliminar una venta
class VentaDeleteView(DeleteView):
    model = Sale
    template_name = 'ventas/venta_confirm_delete.html'
    success_url = reverse_lazy('venta_list')






# Vista para listar precios de venta
class PrecioVentaListView(ListView):
    model = PrecioVenta
    template_name = 'ventas/precioventa_list.html'
    context_object_name = 'precios'

# Vista para crear un precio de venta
class PrecioVentaCreateView(CreateView):
    model = PrecioVenta
    form_class = PrecioVentaForm
    template_name = 'ventas/precioventa_form.html'
    success_url = reverse_lazy('precioventa_list')

# Vista para actualizar un precio de venta
class PrecioVentaUpdateView(UpdateView):
    model = PrecioVenta
    form_class = PrecioVentaForm
    template_name = 'ventas/precioventa_form.html'
    success_url = reverse_lazy('precioventa_list')

# Vista para eliminar un precio de venta
class PrecioVentaDeleteView(DeleteView):
    model = PrecioVenta
    template_name = 'ventas/precioventa_confirm_delete.html'
    success_url = reverse_lazy('precioventa_list')





# Vista para listar comisiones de vendedores
class ComisionVendedorListView(ListView):
    model = ComisionVendedor
    template_name = 'ventas/comisionvendedor_list.html'
    context_object_name = 'comisiones'

# Vista para crear una comisión de vendedor
class ComisionVendedorCreateView(CreateView):
    model = ComisionVendedor
    form_class = ComisionVendedorForm
    template_name = 'ventas/comisionvendedor_form.html'
    success_url = reverse_lazy('comision_list')

# Vista para actualizar una comisión de vendedor
class ComisionVendedorUpdateView(UpdateView):
    model = ComisionVendedor
    form_class = ComisionVendedorForm
    template_name = 'ventas/comisionvendedor_form.html'
    success_url = reverse_lazy('comision_list')

# Vista para eliminar una comisión de vendedor
class ComisionVendedorDeleteView(DeleteView):
    model = ComisionVendedor
    template_name = 'ventas/comision_eliminar.html'
    success_url = reverse_lazy('comision_list')