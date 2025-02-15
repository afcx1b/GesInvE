from django.urls import path
from . import views

app_name = "catalogs"

urlpatterns = [
    path('offers/', views.offer_list, name='offers_list'),
    path('offers/create/', views.create_offer, name='offer_create'),
    path('offers/edit/<int:offer_id>/', views.edit_offer, name='offer_edit'),
    path('offers/delete/<int:offer_id>/', views.delete_offer, name='offer_delete'),
    
    path('orders/', views.order_list, name='orders_list'),
    path('orders/create/', views.create_order, name='order_create'),
    path('orders/edit/<int:order_id>/', views.edit_order, name='order_edit'),
    path('orders/delete/<int:order_id>/', views.delete_order, name='order_delete'),
    
    path('banners/', views.banner_list, name='banners_list'),
    path('banners/create/', views.create_banner, name='banner_create'),
    path('banners/edit/<int:banner_id>/', views.edit_banner, name='banner_edit'),
    path('banners/delete/<int:banner_id>/', views.delete_banner, name='banner_delete'),
    
    path('category/<int:id>/', views.catalog_by_category, name='catalog_by_category'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),

    # Nuevas URLs para Catálogos
    path('catalogs/', views.catalog_list, name='catalog_list'),
    path('catalogs/create/', views.create_catalog, name='catalog_create'),
    path('catalogs/edit/<int:catalog_id>/', views.edit_catalog, name='catalog_edit'),
    path('catalogs/delete/<int:catalog_id>/', views.delete_catalog, name='catalog_delete'),

    # Nuevas URLs para Productos de Catálogos
    path('catalog-products/', views.catalog_product_list, name='catalog_product_list'),
    path('catalog-products/create/', views.create_catalog_product, name='catalog_product_create'),
    path('catalog-products/edit/<int:catalog_product_id>/', views.edit_catalog_product, name='catalog_product_edit'),
    path('catalog-products/delete/<int:catalog_product_id>/', views.delete_catalog_product, name='catalog_product_delete'),
]
