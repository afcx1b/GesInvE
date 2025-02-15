from django import forms
from .models import Category
 
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category', 'parent']
        widgets = {
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la categoría'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
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
 