from django.contrib import admin
from .models import Position, Employee, User, Customer

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('idPosition', 'position')
    search_fields = ('position',)
    list_filter = ('position',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('idEmployee', 'name', 'surname', 'dni', 'phone', 'email', 'idPosition')
    search_fields = ('name', 'surname', 'dni', 'email')
    list_filter = ('idPosition',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('idUser', 'username', 'email', 'idEmployee')
    search_fields = ('username', 'email')
    list_filter = ('idEmployee',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('idCustomer', 'name', 'surname', 'phone', 'email')
    search_fields = ('name', 'surname', 'email')
    list_filter = ('name', 'surname')