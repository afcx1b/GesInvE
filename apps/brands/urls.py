from django.urls import path
from .views import BrandListView, BrandCreateView, BrandUpdateView, BrandDeleteView

app_name = "brands"

urlpatterns = [
    path("brands/", BrandListView.as_view(), name="brands_list"),
    path("brands/new/", BrandCreateView.as_view(), name="brand_create"),
    path("brands/edit/<int:pk>/", BrandUpdateView.as_view(), name="brand_edit"),
    path("brands/delete/<int:pk>/", BrandDeleteView.as_view(), name="brand_delete"),
]