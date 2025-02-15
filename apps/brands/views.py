from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Brand
from .forms import BrandForm

class BrandListView(ListView):
    model = Brand
    template_name = "brands/brands_list.html"
    context_object_name = "brands"
    ordering = ["-idBrand"]  # Ordena de más reciente a más antiguo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Marcas', 'url': reverse_lazy('brands:brands_list')}
        ]
        return context

class BrandCreateView(CreateView):
    model = Brand
    form_class = BrandForm
    template_name = "brands/brand_form.html"
    success_url = reverse_lazy("brands:brands_list")

    def form_valid(self, form):
        messages.success(self.request, "Marca creada exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear la marca. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['breadcrumb'] = [
            {'name': 'Marcas', 'url': reverse_lazy('brands:brands_list')},
            {'name': 'Nueva Marca', 'url': ''}
        ]
        return context

class BrandUpdateView(UpdateView):
    model = Brand
    form_class = BrandForm
    template_name = "brands/brand_form.html"
    success_url = reverse_lazy("brands:brands_list")

    def form_valid(self, form):
        messages.success(self.request, "Marca actualizada exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar la marca. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.all()
        context['breadcrumb'] = [
            {'name': 'Marcas', 'url': reverse_lazy('brands:brands_list')},
            {'name': 'Editar Marca', 'url': ''}
        ]
        return context

class BrandDeleteView(DeleteView):
    model = Brand
    template_name = "brands/brand_confirm_delete.html"
    success_url = reverse_lazy("brands:brands_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Marca eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Marcas', 'url': reverse_lazy('brands:brands_list')},
            {'name': 'Eliminar Marca', 'url': ''}
        ]
        return context