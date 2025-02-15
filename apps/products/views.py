from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages

from apps.brands.models import Brand
from apps.cashier.models import Unit
from apps.categories.models import Category
from .models import Product
from .forms import ProductForm

class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    ordering = ["-idProduct"]

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(product__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['breadcrumb'] = [
            {'name': 'Productos', 'url': reverse_lazy('products:products_list')}
        ]
        return context

class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:products_list")

    def form_valid(self, form):
        messages.success(self.request, "Producto creado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el producto. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['units'] = Unit.objects.all()
        context['brands'] = Brand.objects.all()
        context['breadcrumb'] = [
            {'name': 'Productos', 'url': reverse_lazy('products:products_list')},
            {'name': 'Nuevo Producto', 'url': ''}
        ]
        return context

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy("products:products_list")

    def form_valid(self, form):
        messages.success(self.request, "Producto actualizado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el producto. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['units'] = Unit.objects.all()
        context['brands'] = Brand.objects.all()
        context['breadcrumb'] = [
            {'name': 'Productos', 'url': reverse_lazy('products:products_list')},
            {'name': 'Editar Producto', 'url': ''}
        ]
        return context

class ProductDeleteView(DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy("products:products_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Producto eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Productos', 'url': reverse_lazy('products:products_list')},
            {'name': 'Eliminar Producto', 'url': ''}
        ]
        return context