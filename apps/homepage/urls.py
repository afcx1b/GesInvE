from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/<int:id>/', views.catalog_detail, name='catalog_detail'),
]
