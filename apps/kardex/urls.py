from django.urls import path
from .views import (
    KardexListView, KardexCreateView, KardexUpdateView, KardexDeleteView,
    CostoListView, CostoCreateView, CostoUpdateView, CostoDeleteView,
    PrecioListView, PrecioCreateView, PrecioUpdateView, PrecioDeleteView
)

app_name = 'kardex'

urlpatterns = [
    path('kardex/', KardexListView.as_view(), name='kardex_list'),
    path('kardex/create/', KardexCreateView.as_view(), name='kardex_create'),
    path('kardex/update/<int:pk>/', KardexUpdateView.as_view(), name='kardex_update'),
    path('kardex/delete/<int:pk>/', KardexDeleteView.as_view(), name='kardex_delete'),
    path('costo/', CostoListView.as_view(), name='costo_list'),
    path('costo/create/', CostoCreateView.as_view(), name='costo_create'),
    path('costo/update/<int:pk>/', CostoUpdateView.as_view(), name='costo_update'),
    path('costo/delete/<int:pk>/', CostoDeleteView.as_view(), name='costo_delete'),
    path('precio/', PrecioListView.as_view(), name='precio_list'),
    path('precio/create/', PrecioCreateView.as_view(), name='precio_create'),
    path('precio/update/<int:pk>/', PrecioUpdateView.as_view(), name='precio_update'),
    path('precio/delete/<int:pk>/', PrecioDeleteView.as_view(), name='precio_delete'),
]