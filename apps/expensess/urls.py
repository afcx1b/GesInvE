from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_gastos, name='lista_gastos'),
    path('nuevo/', views.agregar_gasto, name='agregar_gasto'),
    path('<int:gasto_id>/editar/', views.editar_gasto, name='editar_gasto'),
    path('<int:gasto_id>/eliminar/', views.eliminar_gasto, name='eliminar_gasto'),
]
