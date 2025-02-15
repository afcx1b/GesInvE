from django import forms
from .models import Offer, OfferDetail, Order, OrderDetail, Banner, Catalog, CatalogProduct
from apps.products.models import Product  # Importamos Product de la app products
from apps.categories.models import Category  # Importamos Category de la app categories
from apps.brands.models import Brand  # Importamos Brand de la app brands

# Formulario para gestionar ofertas
class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['title', 'discount_percentage', 'start_date', 'end_date', 'status', 'category', 'is_global']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

# Formulario para gestionar detalles de ofertas
class OfferDetailForm(forms.ModelForm):
    class Meta:
        model = OfferDetail
        fields = ['offer', 'product']

# Formulario para gestionar órdenes
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'order_type', 'status']  # Eliminar 'order_date'

# Formulario para gestionar detalles de órdenes
class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = ['order', 'product', 'quantity', 'price']  # Eliminar 'total_price'

# Formulario para gestionar banners
class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['image', 'url', 'start_date', 'end_date', 'category', 'brand', 'is_active']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

# Formulario para gestionar catálogos
class CatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = ['title', 'image']

# Formulario para gestionar productos de catálogos
class CatalogProductForm(forms.ModelForm):
    product_image = forms.ImageField(label='Imagen del Producto', required=False, widget=forms.FileInput(attrs={'readonly': 'readonly'}))
    pvp = forms.DecimalField(label='PVP', required=False, widget=forms.NumberInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = CatalogProduct
        fields = ['catalog', 'product', 'order', 'product_image']

    def __init__(self, *args, **kwargs):
        super(CatalogProductForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['product_image'].initial = self.instance.product.image.url
