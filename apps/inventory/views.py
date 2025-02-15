from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.db import connection

from .models import Ubicacion, InventarioInicial, MovimientoUbicacion, BajaArticulo, Inventario
from .forms import UbicacionForm, InventarioInicialForm, MovimientoUbicacionForm, BajaArticuloForm, InventarioForm

class InventarioListView(ListView):
    model = Inventario
    template_name = "inventory/inventory_list.html"
    context_object_name = "inventarios"
    ordering = ["-id"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Inventarios', 'url': reverse_lazy('inventory:inventory_list')}
        ]
        return context

class InventarioCreateView(CreateView):
    model = Inventario
    form_class = InventarioForm
    template_name = "inventory/inventory_form.html"
    success_url = reverse_lazy("inventory:inventory_list")

    def form_valid(self, form):
        # Acción adicional antes de guardar el formulario
        # ...tu código aquí...
        self.registrar_inventario_inicial()
        messages.success(self.request, "Inventario creado exitosamente.")
        return super().form_valid(form)

    def registrar_inventario_inicial(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM registrarInventarioInicial")
            result = cursor.fetchall()
            # Procesar el resultado si es necesario
            # ...tu código aquí...

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el inventario. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Inventarios', 'url': reverse_lazy('inventory:inventory_list')},
            {'name': 'Nuevo Inventario', 'url': ''}
        ]
        return context

class InventarioUpdateView(UpdateView):
    model = Inventario
    form_class = InventarioForm
    template_name = "inventory/inventory_form.html"
    success_url = reverse_lazy("inventory:inventory_list")

    def form_valid(self, form):
        messages.success(self.request, "Inventario actualizado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el inventario. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Inventarios', 'url': reverse_lazy('inventory:inventory_list')},
            {'name': 'Editar Inventario', 'url': ''}
        ]
        return context

class InventarioDeleteView(DeleteView):
    model = Inventario
    template_name = "inventory/inventory_confirm_delete.html"
    success_url = reverse_lazy("inventory:inventory_list")

    def delete(self, request, *args, **kwargs):
        # Acción adicional antes de eliminar el objeto
        # ...tu código aquí...
        messages.success(self.request, "Inventario eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Inventarios', 'url': reverse_lazy('inventory:inventory_list')},
            {'name': 'Eliminar Inventario', 'url': ''}
        ]
        return context

class UbicacionListView(ListView):
    model = Ubicacion
    template_name = "inventory/ubicacion_list.html"
    context_object_name = "ubicaciones"
    ordering = ["-id"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Ubicaciones', 'url': reverse_lazy('inventory:ubicacion_list')}
        ]
        return context

class UbicacionCreateView(CreateView):
    model = Ubicacion
    form_class = UbicacionForm
    template_name = "inventory/ubicacion_form.html"
    success_url = reverse_lazy("inventory:ubicacion_list")

    def form_valid(self, form):
        # Acción adicional antes de guardar el formulario
        # ...tu código aquí...
        messages.success(self.request, "Ubicación creada exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear la ubicación. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Ubicaciones', 'url': reverse_lazy('inventory:ubicacion_list')},
            {'name': 'Nueva Ubicación', 'url': ''}
        ]
        return context

class UbicacionUpdateView(UpdateView):
    model = Ubicacion
    form_class = UbicacionForm
    template_name = "inventory/ubicacion_form.html"
    success_url = reverse_lazy("inventory:ubicacion_list")

    def form_valid(self, form):
        messages.success(self.request, "Ubicación actualizada exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar la ubicación. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Ubicaciones', 'url': reverse_lazy('inventory:ubicacion_list')},
            {'name': 'Editar Ubicación', 'url': ''}
        ]
        return context

class UbicacionDeleteView(DeleteView):
    model = Ubicacion
    template_name = "inventory/ubicacion_confirm_delete.html"
    success_url = reverse_lazy("inventory:ubicacion_list")

    def delete(self, request, *args, **kwargs):
        # Acción adicional antes de eliminar el objeto
        # ...tu código aquí...
        messages.success(self.request, "Ubicación eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Ubicaciones', 'url': reverse_lazy('inventory:ubicacion_list')},
            {'name': 'Eliminar Ubicación', 'url': ''}
        ]
        return context

class InventarioInicialListView(ListView):
    model = InventarioInicial
    template_name = "inventory/inventarioinicial_list.html"
    context_object_name = "inventariosiniciales"
    ordering = ["-id"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Inventarios Iniciales', 'url': reverse_lazy('inventory:inventarioinicial_list')}
        ]
        return context

class InventarioInicialCreateView(CreateView):
    model = InventarioInicial
    form_class = InventarioInicialForm
    template_name = "inventory/inventarioinicial_form.html"
    success_url = reverse_lazy("inventory:inventarioinicial_list")

    def form_valid(self, form):
        messages.success(self.request, "Inventario Inicial creado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el Inventario Inicial. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Inventarios Iniciales', 'url': reverse_lazy('inventory:inventarioinicial_list')},
            {'name': 'Nuevo Inventario Inicial', 'url': ''}
        ]
        return context

class InventarioInicialUpdateView(UpdateView):
    model = InventarioInicial
    form_class = InventarioInicialForm
    template_name = "inventory/inventarioinicial_form.html"
    success_url = reverse_lazy("inventory:inventarioinicial_list")

    def form_valid(self, form):
        messages.success(self.request, "Inventario Inicial actualizado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el Inventario Inicial. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Inventarios Iniciales', 'url': reverse_lazy('inventory:inventarioinicial_list')},
            {'name': 'Editar Inventario Inicial', 'url': ''}
        ]
        return context

class InventarioInicialDeleteView(DeleteView):
    model = InventarioInicial
    template_name = "inventory/inventarioinicial_confirm_delete.html"
    success_url = reverse_lazy("inventory:inventarioinicial_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Inventario Inicial eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Inventarios Iniciales', 'url': reverse_lazy('inventory:inventarioinicial_list')},
            {'name': 'Eliminar Inventario Inicial', 'url': ''}
        ]
        return context

class MovimientoUbicacionListView(ListView):
    model = MovimientoUbicacion
    template_name = "inventory/movimientoubicacion_list.html"
    context_object_name = "movimientosubicacion"
    ordering = ["-id"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Movimientos de Ubicación', 'url': reverse_lazy('inventory:movimientoubicacion_list')}
        ]
        return context

class MovimientoUbicacionCreateView(CreateView):
    model = MovimientoUbicacion
    form_class = MovimientoUbicacionForm
    template_name = "inventory/movimientoubicacion_form.html"
    success_url = reverse_lazy("inventory:movimientoubicacion_list")

    def form_valid(self, form):
        messages.success(self.request, "Movimiento de Ubicación creado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear el Movimiento de Ubicación. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Movimientos de Ubicación', 'url': reverse_lazy('inventory:movimientoubicacion_list')},
            {'name': 'Nuevo Movimiento de Ubicación', 'url': ''}
        ]
        return context

class MovimientoUbicacionUpdateView(UpdateView):
    model = MovimientoUbicacion
    form_class = MovimientoUbicacionForm
    template_name = "inventory/movimientoubicacion_form.html"
    success_url = reverse_lazy("inventory:movimientoubicacion_list")

    def form_valid(self, form):
        messages.success(self.request, "Movimiento de Ubicación actualizado exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar el Movimiento de Ubicación. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Movimientos de Ubicación', 'url': reverse_lazy('inventory:movimientoubicacion_list')},
            {'name': 'Editar Movimiento de Ubicación', 'url': ''}
        ]
        return context

class MovimientoUbicacionDeleteView(DeleteView):
    model = MovimientoUbicacion
    template_name = "inventory/movimientoubicacion_confirm_delete.html"
    success_url = reverse_lazy("inventory:movimientoubicacion_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Movimiento de Ubicación eliminado exitosamente.")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Movimientos de Ubicación', 'url': reverse_lazy('inventory:movimientoubicacion_list')},
            {'name': 'Eliminar Movimiento de Ubicación', 'url': ''}
        ]
        return context

class BajaArticuloListView(ListView):
    model = BajaArticulo
    template_name = "inventory/bajaarticulo_list.html"
    context_object_name = "bajasarticulo"
    ordering = ["-id"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Bajas de Artículos', 'url': reverse_lazy('inventory:bajaarticulo_list')}
        ]
        return context

class BajaArticuloCreateView(CreateView):
    model = BajaArticulo
    form_class = BajaArticuloForm
    template_name = "inventory/bajaarticulo_form.html"
    success_url = reverse_lazy("inventory:bajaarticulo_list")

    def form_valid(self, form):
        # Acción adicional antes de guardar el formulario
        # ...tu código aquí...
        self.registrar_baja_articulos()
        messages.success(self.request, "Baja de Artículo creada exitosamente.")
        return super().form_valid(form)

    def registrar_baja_articulos(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM registrarBajaArticulos")
            result = cursor.fetchall()
            # Procesar el resultado si es necesario
            # ...tu código aquí...

    def form_invalid(self, form):
        messages.error(self.request, "Error al crear la Baja de Artículo. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Bajas de Artículos', 'url': reverse_lazy('inventory:bajaarticulo_list')},
            {'name': 'Nueva Baja de Artículo', 'url': ''}
        ]
        return context

class BajaArticuloUpdateView(UpdateView):
    model = BajaArticulo
    form_class = BajaArticuloForm
    template_name = "inventory/bajaarticulo_form.html"
    success_url = reverse_lazy("inventory:bajaarticulo_list")

    def form_valid(self, form):
        messages.success(self.request, "Baja de Artículo actualizada exitosamente.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al actualizar la Baja de Artículo. Verifique los datos.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Bajas de Artículos', 'url': reverse_lazy('inventory:bajaarticulo_list')},
            {'name': 'Editar Baja de Artículo', 'url': ''}
        ]
        return context

class BajaArticuloDeleteView(DeleteView):
    model = BajaArticulo
    template_name = "inventory/bajaarticulo_confirm_delete.html"
    success_url = reverse_lazy("inventory:bajaarticulo_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Baja de Artículo eliminada exitosamente.")
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'name': 'Bajas de Artículos', 'url': reverse_lazy('inventory:bajaarticulo_list')},
            {'name': 'Eliminar Baja de Artículo', 'url': ''}
        ]
        return context
