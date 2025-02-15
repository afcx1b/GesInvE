from django import forms
from .models import Ubicacion, InventarioInicial, MovimientoUbicacion, BajaArticulo, Inventario

class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ['nombre', 'codigo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
        }

class InventarioInicialForm(forms.ModelForm):
    class Meta:
        model = InventarioInicial
        fields = ['articulo', 'cantidad', 'costo', 'precio', 'ubicacion']
        widgets = {
            'articulo': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'costo': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.Select(attrs={'class': 'form-control'}),
        }

class MovimientoUbicacionForm(forms.ModelForm):
    class Meta:
        model = MovimientoUbicacion
        fields = ['articulo', 'cantidad', 'ubicacion_origen', 'ubicacion_destino']
        widgets = {
            'articulo': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'ubicacion_origen': forms.Select(attrs={'class': 'form-control'}),
            'ubicacion_destino': forms.Select(attrs={'class': 'form-control'}),
        }

class BajaArticuloForm(forms.ModelForm):
    class Meta:
        model = BajaArticulo
        fields = ['articulo', 'cantidad', 'motivo']
        widgets = {
            'articulo': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control'}),
        }

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['articulo', 'cantidad_disponible']
        widgets = {
            'articulo': forms.Select(attrs={'class': 'form-control'}),
            'cantidad_disponible': forms.NumberInput(attrs={'class': 'form-control'}),
        }
