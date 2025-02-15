from django import forms
from .models import ConfiguracionGeneral, Unit, Cashier

# Formulario para gestionar configuraciones generales
class ConfiguracionGeneralForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionGeneral
        fields = ['nombre_sistema', 'logo', 'moneda', 'impuesto', 'precio1', 'precio2', 'precio3']

# Formulario para gestionar unidades
class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['unit']

# Formulario para gestionar cajeros
class CashierForm(forms.ModelForm):
    class Meta:
        model = Cashier
        fields = ['idUser', 'cashier', 'serialNumber']
