from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['idCategory', 'idUnit', 'barcode', 'product', 'idMarca', 'imagen']
        widgets = {
            'idCategory': forms.Select(attrs={'class': 'form-control'}),
            'idUnit': forms.Select(attrs={'class': 'form-control'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control'}),
            'product': forms.TextInput(attrs={'class': 'form-control'}),
            'idMarca': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        """Genera el barcode si está vacío y se ha seleccionado una categoría."""
        cleaned_data = super().clean()
        barcode = cleaned_data.get('barcode')
        category = cleaned_data.get('idCategory')

        if not barcode and category:
            last_product = Product.objects.filter(idCategory=category).order_by('-barcode').first()
            last_code = int(last_product.barcode[-3:]) + 1 if last_product and last_product.barcode else 1
            cleaned_data['barcode'] = f"{category.codigo_base}{last_code:03d}"

        return cleaned_data
