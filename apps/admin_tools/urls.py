from django.urls import path
from apps.admin_tools.views import CompanyUpdateView, export_data, import_data


urlpatterns = [
    path('export/', export_data, name='export_data'),
    path('import/', import_data, name='import_data'),
    path('company/update/', CompanyUpdateView.as_view(), name='company_update'),

]
