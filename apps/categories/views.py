from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Category
from .forms import CategoryForm

class CategoryListView(ListView):
    model = Category
    template_name = "categories/category_list.html"
    context_object_name = "categories"
    ordering = ["-idCategory"]  # Ordena de más reciente a más antiguo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Categorías', 'url': reverse_lazy('categories:categories_list')}
        ]
        return context    
 
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/category_form.html"
    success_url = reverse_lazy("categories:category_create")

    def form_valid(self, form):
        messages.success(self.request, "Categoría creada exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear la categoría. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['breadcrumb'] = [
            {'name': 'Categorías', 'url': reverse_lazy('categories:category_create')},
            {'name': 'Nueva Categoría', 'url': ''}
        ]
        return context
    
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "categories/category_form.html"
    success_url = reverse_lazy("categories:categories_list")

    def form_valid(self, form):
        messages.success(self.request, "Categoría actualizada exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar la categoría. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['breadcrumb'] = [
            {'name': 'Categorías', 'url': reverse_lazy('categories:categories_list')},
            {'name': 'Editar Categoría', 'url': ''}
        ]
        return context
    
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "categories/category_confirm_delete.html"
    success_url = reverse_lazy("categories:categories_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Categoría eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Categorías', 'url': reverse_lazy('categories:categories_list')},
            {'name': 'Eliminar Categoría', 'url': ''}
        ]
        return context
    
def category_form_view(request):
    last_parent_category = request.session.get('last_parent_category', None)
    form = CategoryForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        request.session['last_parent_category'] = form.cleaned_data['parent'].idCategory if form.cleaned_data['parent'] else None
        messages.success(request, "Categoría guardada exitosamente.")
        return redirect('categories:category_form_view')
    categories = Category.objects.all()
    return render(request, 'categories/category_form.html', {
        'form': form,
        'last_parent_category': last_parent_category,
        'categories': categories,
    })