from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import ConfiguracionGeneral, Unit, Cashier
from .forms import ConfiguracionGeneralForm, UnitForm, CashierForm

class ConfiguracionGeneralView(UpdateView):
    model = ConfiguracionGeneral
    form_class = ConfiguracionGeneralForm
    template_name = "cashier/configuracion_general_form.html"
    success_url = reverse_lazy("cashier:configuracion_general")

    def form_valid(self, form):
        messages.success(self.request, "Configuración general actualizada exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar la configuración general. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Configuración General', 'url': reverse_lazy('cashier:configuracion_general')}
        ]
        return context

class UnitListView(ListView):
    model = Unit
    template_name = "cashier/unit_list.html"
    context_object_name = "units"
    ordering = ["-idUnit"]  # Ordena de más reciente a más antiguo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Unidades', 'url': reverse_lazy('cashier:unit_list')}
        ]
        return context

class UnitCreateView(CreateView):
    model = Unit
    form_class = UnitForm
    template_name = "cashier/unit_form.html"
    success_url = reverse_lazy("cashier:unit_list")

    def form_valid(self, form):
        messages.success(self.request, "Unidad creada exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear la unidad. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['units'] = Unit.objects.all()
        context['breadcrumb'] = [
            {'name': 'Unidades', 'url': reverse_lazy('cashier:unit_list')},
            {'name': 'Nueva Unidad', 'url': ''}
        ]
        return context

class UnitUpdateView(UpdateView):
    model = Unit
    form_class = UnitForm
    template_name = "cashier/unit_form.html"
    success_url = reverse_lazy("cashier:unit_list")

    def form_valid(self, form):
        messages.success(self.request, "Unidad actualizada exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar la unidad. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['units'] = Unit.objects.all()
        context['breadcrumb'] = [
            {'name': 'Unidades', 'url': reverse_lazy('cashier:unit_list')},
            {'name': 'Editar Unidad', 'url': ''}
        ]
        return context

class UnitDeleteView(DeleteView):
    model = Unit
    template_name = "cashier/unit_confirm_delete.html"
    success_url = reverse_lazy("cashier:unit_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Unidad eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Unidades', 'url': reverse_lazy('cashier:unit_list')},
            {'name': 'Eliminar Unidad', 'url': ''}
        ]
        return context

class CashierListView(ListView):
    model = Cashier
    template_name = "cashier/cashier_list.html"
    context_object_name = "cashiers"
    ordering = ["-idCashier"]  # Ordena de más reciente a más antiguo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Cajeros', 'url': reverse_lazy('cashier:cashier_list')}
        ]
        return context

class CashierCreateView(CreateView):
    model = Cashier
    form_class = CashierForm
    template_name = "cashier/cashier_form.html"
    success_url = reverse_lazy("cashier:cashier_list")

    def form_valid(self, form):
        messages.success(self.request, "Cajero creado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el cajero. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cashiers'] = Cashier.objects.all()
        context['breadcrumb'] = [
            {'name': 'Cajeros', 'url': reverse_lazy('cashier:cashier_list')},
            {'name': 'Nuevo Cajero', 'url': ''}
        ]
        return context

class CashierUpdateView(UpdateView):
    model = Cashier
    form_class = CashierForm
    template_name = "cashier/cashier_form.html"
    success_url = reverse_lazy("cashier:cashier_list")

    def form_valid(self, form):
        messages.success(self.request, "Cajero actualizado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el cajero. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cashiers'] = Cashier.objects.all()
        context['breadcrumb'] = [
            {'name': 'Cajeros', 'url': reverse_lazy('cashier:cashier_list')},
            {'name': 'Editar Cajero', 'url': ''}
        ]
        return context

class CashierDeleteView(DeleteView):
    model = Cashier
    template_name = "cashier/cashier_confirm_delete.html"
    success_url = reverse_lazy("cashier:cashier_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Cajero eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Cajeros', 'url': reverse_lazy('cashier:cashier_list')},
            {'name': 'Eliminar Cajero', 'url': ''}
        ]
        return context