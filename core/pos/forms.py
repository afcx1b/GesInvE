from django import forms
from django.forms import ModelForm

from core.pos.models import *


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = ['parent', 'category']
        widgets = {
            'parent': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),

        }
 
    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        parent = cleaned_data.get("parent")

        # Validación para evitar nombres duplicados (Django ya lo impide, pero esto da un mensaje más claro)
        #if Category.objects.filter(category=category).exclude(idCategory=self.instance.#idCategory).exists():
        #    self.add_error("category", "Ya existe una categoría con este nombre.")

        # Validación de jerarquía: No se puede asignar como padre una categoría de nivel inferior
        if parent and parent.parent and parent.parent.parent and parent.parent.parent.parent:
            self.add_error("parent", "No se pueden crear más de 4 niveles en la jerarquía.")

        return cleaned_data

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ingrese un nombre',
            }),
            'category': forms.Select(attrs={
                'class': 'select2',
                'style': 'width: 100%'
            }),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'names': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'dni': forms.TextInput(attrs={'placeholder': 'Ingrese un número de cedula'}),
            'birthdate': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'birthdate',
                'value': datetime.now().strftime('%Y-%m-%d'),
                'data-toggle': 'datetimepicker',
                'data-target': '#birthdate'
            }),
            'address': forms.TextInput(attrs={
                'placeholder': 'Ingrese una dirección',
            }),
            'gender': forms.Select(attrs={
                'class': 'select2',
                'style': 'width: 100%'
            })
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.none()

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'client': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={
                'value': datetime.now().strftime('%Y-%m-%d'),
                'autocomplete': 'off',
                'class': 'form-control datetimepicker-input',
                'id': 'date_joined',
                'data-target': '#date_joined',
                'data-toggle': 'datetimepicker'
            }
                                           ),
            'iva': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            })
        }


class CompanyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Company
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'ruc': forms.TextInput(attrs={'placeholder': 'Ingrese un ruc'}),
            'address': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono celular'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono convencional'}),
            'website': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección web'}),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
