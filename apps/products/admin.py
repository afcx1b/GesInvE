from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('idProduct', 'product', 'idCategory', 'idMarca', 'barcode', 'idUnit', 'is_new')
    search_fields = ('product', 'barcode', 'idCategory__category', 'idMarca__brand')
    list_filter = ('idCategory', 'idMarca', 'is_new')
    ordering = ('-idCategory', 'product', 'idMarca')