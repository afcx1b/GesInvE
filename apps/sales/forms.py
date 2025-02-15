from django import forms
from .models import Cliente, Sale, SaleProduct, PrecioVenta, ComisionVendedor

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'cedula', 'direccion', 'telefono', 'email', 'facebook', 'instagram', 'whatsapp']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 2}),
        }

class VentaForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['cliente', 'usuario', 'tipo', 'metodo_pago']

class SaleProductForm(forms.ModelForm):
    class Meta:
        model = SaleProduct
        fields = ['venta', 'articulo', 'cantidad', 'precio', 'tipo_precio']

class PrecioVentaForm(forms.ModelForm):
    class Meta:
        model = PrecioVenta
        fields = ['articulo', 'tipo', 'porcentaje_aumento', 'fecha_inicio', 'fecha_fin']

class ComisionVendedorForm(forms.ModelForm):
    class Meta:
        model = ComisionVendedor
        fields = ['vendedor', 'porcentaje_comision', 'fecha_inicio', 'fecha_fin']
