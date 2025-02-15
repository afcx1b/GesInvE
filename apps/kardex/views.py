from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect, render
from apps.kardex.models import Kardex, Costo, Precio
from apps.kardex.forms import KardexForm, CostoForm, PrecioForm

class KardexListView(ListView):
    model = Kardex
    template_name = "kardex/kardex_list.html"
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Kardex', 'url': reverse_lazy('kardex:kardex_list')}
        ]
        return context

class KardexCreateView(CreateView):
    model = Kardex
    form_class = KardexForm
    template_name = "kardex/kardex_form.html"
    success_url = reverse_lazy("kardex:kardex_create")

    def form_valid(self, form):
        messages.success(self.request, "Kardex creado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el Kardex. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Kardex.objects.all()
        context['breadcrumb'] = [
            {'name': 'Kardex', 'url': reverse_lazy('kardex:kardex_create')},
            {'name': 'Nuevo Kardex', 'url': ''}
        ]
        return context

class KardexUpdateView(UpdateView):
    model = Kardex
    form_class = KardexForm
    template_name = "kardex/kardex_form.html"
    success_url = reverse_lazy("kardex:kardex_list")

    def form_valid(self, form):
        messages.success(self.request, "Kardex actualizado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el Kardex. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Kardex.objects.all()
        context['breadcrumb'] = [
            {'name': 'Kardex', 'url': reverse_lazy('kardex:kardex_list')},
            {'name': 'Editar Kardex', 'url': ''}
        ]
        return context

class KardexDeleteView(DeleteView):
    model = Kardex
    template_name = "kardex/kardex_confirm_delete.html"
    success_url = reverse_lazy("kardex:kardex_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Kardex eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Kardex', 'url': reverse_lazy('kardex:kardex_list')},
            {'name': 'Eliminar Kardex', 'url': ''}
        ]
        return context

class CostoListView(ListView):
    model = Costo
    template_name = "kardex/costo_list.html"
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Costo', 'url': reverse_lazy('kardex:costo_list')}
        ]
        return context

class CostoCreateView(CreateView):
    model = Costo
    form_class = CostoForm
    template_name = "kardex/costo_form.html"
    success_url = reverse_lazy("kardex:costo_create")

    def form_valid(self, form):
        messages.success(self.request, "Costo creado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el Costo. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Costo.objects.all()
        context['breadcrumb'] = [
            {'name': 'Costo', 'url': reverse_lazy('kardex:costo_create')},
            {'name': 'Nuevo Costo', 'url': ''}
        ]
        return context

class CostoUpdateView(UpdateView):
    model = Costo
    form_class = CostoForm
    template_name = "kardex/costo_form.html"
    success_url = reverse_lazy("kardex:costo_list")

    def form_valid(self, form):
        messages.success(self.request, "Costo actualizado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el Costo. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Costo.objects.all()
        context['breadcrumb'] = [
            {'name': 'Costo', 'url': reverse_lazy('kardex:costo_list')},
            {'name': 'Editar Costo', 'url': ''}
        ]
        return context

class CostoDeleteView(DeleteView):
    model = Costo
    template_name = "kardex/costo_confirm_delete.html"
    success_url = reverse_lazy("kardex:costo_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Costo eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Costo', 'url': reverse_lazy('kardex:costo_list')},
            {'name': 'Eliminar Costo', 'url': ''}
        ]
        return context

class PrecioListView(ListView):
    model = Precio
    template_name = "kardex/precio_list.html"
    context_object_name = "items"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Precio', 'url': reverse_lazy('kardex:precio_list')}
        ]
        return context

class PrecioCreateView(CreateView):
    model = Precio
    form_class = PrecioForm
    template_name = "kardex/precio_form.html"
    success_url = reverse_lazy("kardex:precio_create")

    def form_valid(self, form):
        messages.success(self.request, "Precio creado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el Precio. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Precio.objects.all()
        context['breadcrumb'] = [
            {'name': 'Precio', 'url': reverse_lazy('kardex:precio_create')},
            {'name': 'Nuevo Precio', 'url': ''}
        ]
        return context

class PrecioUpdateView(UpdateView):
    model = Precio
    form_class = PrecioForm
    template_name = "kardex/precio_form.html"
    success_url = reverse_lazy("kardex:precio_list")

    def form_valid(self, form):
        messages.success(self.request, "Precio actualizado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el Precio. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = Precio.objects.all()
        context['breadcrumb'] = [
            {'name': 'Precio', 'url': reverse_lazy('kardex:precio_list')},
            {'name': 'Editar Precio', 'url': ''}
        ]
        return context

class PrecioDeleteView(DeleteView):
    model = Precio
    template_name = "kardex/precio_confirm_delete.html"
    success_url = reverse_lazy("kardex:precio_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Precio eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Precio', 'url': reverse_lazy('kardex:precio_list')},
            {'name': 'Eliminar Precio', 'url': ''}
        ]
        return context