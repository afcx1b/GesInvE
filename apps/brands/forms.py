from django import forms
from .models import Brand

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand']
        labels = {
            'brand': 'Marca'
        }
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la marca'}),

        }
 