from django.contrib import admin
from .models import ConfiguracionGeneral, Unit, Cashier

@admin.register(ConfiguracionGeneral)
class ConfiguracionGeneralAdmin(admin.ModelAdmin):
    list_display = ('nombre_sistema', 'moneda', 'impuesto', 'precio1', 'precio2', 'precio3')
    search_fields = ('nombre_sistema', 'moneda')
    list_filter = ('moneda',)

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('idUnit', 'unit')
    search_fields = ('unit',)

@admin.register(Cashier)
class CashierAdmin(admin.ModelAdmin):
    list_display = ('idCashier', 'cashier', 'serialNumber', 'idUser')
    search_fields = ('cashier', 'serialNumber', 'idUser__username')
    list_filter = ('idUser',)