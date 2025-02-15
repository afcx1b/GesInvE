import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm
from django.contrib.auth.decorators import login_required, permission_required
from django.apps import apps
import io
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import CompanyForm
from .mixins import ValidatePermissionRequiredMixin
from .models import Company

@login_required
@permission_required('admin_tools.can_manage_data', raise_exception=True)
def export_data(request):
    """Exporta los datos de la base de datos a un archivo Excel."""
    if request.method == "POST":
        app_label = request.POST.get("app_label")
        table_name = request.POST.get("table")
        format_type = request.POST.get("format", "xlsx")
        
        if table_name == "all":
            tables = apps.get_models()
        else:
            tables = [apps.get_model(app_label=app_label, model_name=table_name)]

        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')

        for table in tables:
            data = table.objects.all().values()
            df = pd.DataFrame(list(data))
            # Asegurarse de que los datetimes no tengan información de zona horaria
            for column in df.select_dtypes(include=['datetime']):
                df[column] = df[column].dt.tz_localize(None)
            df.to_excel(writer, sheet_name=table._meta.db_table, index=False)

        writer.close()
        output.seek(0)

        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = f'attachment; filename="{table_name}_data.xlsx"'
        return response

    return render(request, "admin_tools/export.html")

@login_required
@permission_required('admin_tools.can_manage_data', raise_exception=True)
def import_data(request):
    """Importa datos desde un archivo Excel a la base de datos."""
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            df = pd.read_excel(file)
            app_label = request.POST.get("app_label")
            table_name = request.POST.get("table")

            model = apps.get_model(app_label=app_label, model_name=table_name)

            try:
                model.objects.bulk_create([model(**row) for row in df.to_dict(orient="records")])
                return HttpResponse("Datos importados correctamente.")
            except Exception as e:
                return HttpResponse(f"Error al importar datos: {e}", status=400)
    else:
        form = UploadFileForm()
    
    return render(request, "admin_tools/import.html", {"form": form})


 

class CompanyUpdateView(ValidatePermissionRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company/create.html'
    success_url = reverse_lazy('dashboard')
    url_redirect = success_url
    permission_required = 'change_company'

    def get_object(self, queryset=None):
        company = Company.objects.all()
        if company.exists():
            return company[0]
        return Company()

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                instance = self.get_object()
                if instance.pk is not None:
                    form = CompanyForm(request.POST, request.FILES, instance=instance)
                    data = form.save()
                else:
                    form = CompanyForm(request.POST, request.FILES)
                    data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de mi compañia'
        context['entity'] = 'Compañia'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
