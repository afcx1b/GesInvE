from django.contrib import admin
from .models import Brand

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('idBrand', 'brand')
    search_fields = ('brand',)
    ordering = ('brand',)