from django import forms
from apps.kardex.models import Kardex, Costo, Precio

class KardexForm(forms.ModelForm):
    class Meta:
        model = Kardex
        fields = '__all__'
        widgets = {
            'articulo': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo_movimiento': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'costo_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CostoForm(forms.ModelForm):
    class Meta:
        model = Costo
        fields = '__all__'
        widgets = {
            'articulo': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'costo_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PrecioForm(forms.ModelForm):
    class Meta:
        model = Precio
        fields = '__all__'
        widgets = {
            'articulo': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control'}),
        }
