from django.urls import path
from .views import ConfiguracionGeneralView, UnitListView, UnitCreateView, UnitUpdateView, UnitDeleteView, CashierListView, CashierCreateView, CashierUpdateView, CashierDeleteView

app_name = "cashier"

urlpatterns = [
    path("configuracion_general/", ConfiguracionGeneralView.as_view(), name="configuracion_general"),
    path("units/", UnitListView.as_view(), name="units_list"),
    path("units/new/", UnitCreateView.as_view(), name="unit_create"),
    path("units/edit/<int:pk>/", UnitUpdateView.as_view(), name="unit_edit"),
    path("units/delete/<int:pk>/", UnitDeleteView.as_view(), name="unit_delete"),
    path("cashiers/", CashierListView.as_view(), name="cashiers_list"),
    path("cashiers/new/", CashierCreateView.as_view(), name="cashier_create"),
    path("cashiers/edit/<int:pk>/", CashierUpdateView.as_view(), name="cashier_edit"),
    path("cashiers/delete/<int:pk>/", CashierDeleteView.as_view(), name="cashier_delete"),
]