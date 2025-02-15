from django.urls import path
from .views import (
    UbicacionListView, UbicacionCreateView, UbicacionUpdateView, UbicacionDeleteView,
    InventarioInicialListView, InventarioInicialCreateView, InventarioInicialUpdateView, InventarioInicialDeleteView,
    MovimientoUbicacionListView, MovimientoUbicacionCreateView, MovimientoUbicacionUpdateView, MovimientoUbicacionDeleteView,
    BajaArticuloListView, BajaArticuloCreateView, BajaArticuloUpdateView, BajaArticuloDeleteView,
    InventarioListView, InventarioCreateView, InventarioUpdateView, InventarioDeleteView
)

app_name = "inventory"

urlpatterns = [
    path("ubicaciones/", UbicacionListView.as_view(), name="ubicacion_list"),
    path("ubicaciones/new/", UbicacionCreateView.as_view(), name="ubicacion_create"),
    path("ubicaciones/edit/<int:pk>/", UbicacionUpdateView.as_view(), name="ubicacion_edit"),
    path("ubicaciones/delete/<int:pk>/", UbicacionDeleteView.as_view(), name="ubicacion_delete"),
    path("inventarioinicial/", InventarioInicialListView.as_view(), name="inventarioinicial_list"),
    path("inventarioinicial/new/", InventarioInicialCreateView.as_view(), name="inventarioinicial_create"),
    path("inventarioinicial/edit/<int:pk>/", InventarioInicialUpdateView.as_view(), name="inventarioinicial_edit"),
    path("inventarioinicial/delete/<int:pk>/", InventarioInicialDeleteView.as_view(), name="inventarioinicial_delete"),
    path("movimientoubicacion/", MovimientoUbicacionListView.as_view(), name="movimientoubicacion_list"),
    path("movimientoubicacion/new/", MovimientoUbicacionCreateView.as_view(), name="movimientoubicacion_create"),
    path("movimientoubicacion/edit/<int:pk>/", MovimientoUbicacionUpdateView.as_view(), name="movimientoubicacion_edit"),
    path("movimientoubicacion/delete/<int:pk>/", MovimientoUbicacionDeleteView.as_view(), name="movimientoubicacion_delete"),
    path("bajaarticulo/", BajaArticuloListView.as_view(), name="bajaarticulo_list"),
    path("bajaarticulo/new/", BajaArticuloCreateView.as_view(), name="bajaarticulo_create"),
    path("bajaarticulo/edit/<int:pk>/", BajaArticuloUpdateView.as_view(), name="bajaarticulo_edit"),
    path("bajaarticulo/delete/<int:pk>/", BajaArticuloDeleteView.as_view(), name="bajaarticulo_delete"),
    path("inventory/", InventarioListView.as_view(), name="inventory_list"),
    path("inventory/new/", InventarioCreateView.as_view(), name="inventory_create"),
    path("inventory/edit/<int:pk>/", InventarioUpdateView.as_view(), name="inventory_edit"),
    path("inventory/delete/<int:pk>/", InventarioDeleteView.as_view(), name="inventory_delete"),
]
