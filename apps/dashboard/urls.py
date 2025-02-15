from django.urls import path
from .views import *


urlpatterns = [
    # dashboard
    path('', DashboardView.as_view(), name='dashboard'),
    path('construccion', ConstruccionView.as_view(), name='construccion'),
]