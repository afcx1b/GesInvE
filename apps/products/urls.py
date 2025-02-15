from django.urls import path
from .views import ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = "products"

urlpatterns = [
    path("products/", ProductListView.as_view(), name="products_list"),
    path("products/new/", ProductCreateView.as_view(), name="product_create"),
    path("products/edit/<int:pk>/", ProductUpdateView.as_view(), name="product_edit"),
    path("products/delete/<int:pk>/", ProductDeleteView.as_view(), name="product_delete"),
]