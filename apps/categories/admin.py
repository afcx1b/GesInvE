from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('idCategory', 'category', 'parent', 'codigo_base', 'siglas')
    search_fields = ('category', 'codigo_base', 'siglas')
