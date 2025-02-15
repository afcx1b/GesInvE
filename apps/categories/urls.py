from django.urls import path
from .views import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, category_form_view

app_name = "categories"
 
urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="categories_list"),
    path("categories/new/", CategoryCreateView.as_view(), name="category_create"),
    path("categories/edit/<int:pk>/", CategoryUpdateView.as_view(), name="category_edit"),
    path("categories/delete/<int:pk>/", CategoryDeleteView.as_view(), name="category_delete"),
    path('form/', category_form_view, name='category_form_view'),  # Añade esta línea

]
