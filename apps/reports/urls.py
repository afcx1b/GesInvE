from django.urls import path
from . import views
from apps.reports.views import ReportSaleView

app_name = 'reports'

urlpatterns = [
    path('compras/', views.reportes_compras, name='reporte_compras'),
    path('ventas/', views.reportes_ventas, name='reportes_ventas'),
    path('gastos/', views.reportes_gastos, name='reportes_gastos'),
    path('comisiones/', views.reportes_comisiones, name='reportes_comisiones'),
    path('diario/', views.reporte_diario, name='lista_reportes'),
    path('sale/', ReportSaleView.as_view(), name='sale_report'),
    
]

