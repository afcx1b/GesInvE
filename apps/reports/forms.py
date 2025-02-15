from django import forms
from django.forms import DateInput

class FiltroReporteForm(forms.Form):
    fecha_inicio = forms.DateField(
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha de Inicio"
    )
    fecha_fin = forms.DateField(
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Fecha de Fin"
    )

class ReportForm(forms.Form):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
 