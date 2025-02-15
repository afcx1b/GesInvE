from django.shortcuts import render
from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.utils import timezone
from datetime import date

from apps.purchases.models import Compra, DetalleCompra
from apps.sales.models import Sale, Factura, Ticket, SaleProduct, ComisionVendedor
from apps.expensess.models import Gasto
from .forms import FiltroReporteForm, ReportForm

def reporte_compras(request):
    compras = Compra.objects.all()
    return render(request, 'reportes/reporte_compras.html', {'compras': compras})

def reporte_ventas(request):
    ventas = Sale.objects.all()
    return render(request, 'reportes/reporte_ventas.html', {'ventas': ventas})

def reporte_diario(request):
    hoy = date.today()
    ventas = Sale.objects.filter(fecha=hoy)
    gastos = Gasto.objects.filter(fecha=hoy)
    total_ventas = ventas.aggregate(Sum('total'))['total__sum'] or 0
    total_gastos = gastos.aggregate(Sum('monto'))['monto__sum'] or 0

    return render(request, 'reportes/reporte_diario.html', {
        'ventas': ventas,
        'gastos': gastos,
        'total_ventas': total_ventas,
        'total_gastos': total_gastos,
    })

def reportes_compras(request):
    form = FiltroReporteForm(request.GET or None)
    compras = Compra.objects.all()

    if form.is_valid():
        fecha_inicio = form.cleaned_data['fecha_inicio']
        fecha_fin = form.cleaned_data['fecha_fin']
        compras = compras.filter(fecha__range=[fecha_inicio, fecha_fin])

    total_compras = compras.aggregate(total=Sum('total'))['total'] or 0

    return render(request, 'reportes/reportes_compras.html', {
        'form': form,
        'compras': compras,
        'total_compras': total_compras,
    })

def reportes_ventas(request):
    form = FiltroReporteForm(request.GET or None)
    ventas = list(Ticket.objects.all()) + list(Factura.objects.all())

    if form.is_valid():
        fecha_inicio = form.cleaned_data['fecha_inicio']
        fecha_fin = form.cleaned_data['fecha_fin']
        ventas = [
            venta for venta in ventas
            if fecha_inicio <= venta.fecha.date() <= fecha_fin
        ]

    total_ventas = sum(venta.total for venta in ventas)

    return render(request, 'reportes/reportes_ventas.html', {
        'form': form,
        'ventas': ventas,
        'total_ventas': total_ventas,
    })

def reportes_gastos(request):
    form = FiltroReporteForm(request.GET or None)
    gastos = Gasto.objects.all()

    if form.is_valid():
        fecha_inicio = form.cleaned_data['fecha_inicio']
        fecha_fin = form.cleaned_data['fecha_fin']
        gastos = gastos.filter(fecha__range=[fecha_inicio, fecha_fin])

    total_gastos = gastos.aggregate(total=Sum('monto'))['total'] or 0

    return render(request, 'reportes/reportes_gastos.html', {
        'form': form,
        'gastos': gastos,
        'total_gastos': total_gastos,
    })

def reportes_comisiones(request):
    form = FiltroReporteForm(request.GET or None)
    comisiones = ComisionVendedor.objects.all()

    if form.is_valid():
        fecha_inicio = form.cleaned_data['fecha_inicio']
        fecha_fin = form.cleaned_data['fecha_fin']
        comisiones = comisiones.filter(fecha_inicio__lte=fecha_fin, fecha_fin__gte=fecha_inicio)

    total_comisiones = sum(comision.porcentaje_comision for comision in comisiones)

    return render(request, 'reportes/reportes_comisiones.html', {
        'form': form,
        'comisiones': comisiones,
        'total_comisiones': total_comisiones,
    })

class ReportSaleView(FormView):
    template_name = 'sale/report.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                queryset = Sale.objects.all()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for s in queryset:
                    data.append([
                        s.id,
                        s.client.names,
                        s.date_joined.strftime('%Y-%m-%d'),
                        f'{s.subtotal:.2f}',
                        f'{s.total_iva:.2f}',
                        f'{s.total:.2f}',
                    ])

                subtotal = queryset.aggregate(r=Coalesce(Sum('subtotal'), 0, output_field=FloatField())).get('r')
                iva = queryset.aggregate(r=Coalesce(Sum('iva'), 0, output_field=FloatField())).get('r')
                total = queryset.aggregate(r=Coalesce(Sum('total'), 0, output_field=FloatField())).get('r')

                data.append([
                    '---',
                    '---',
                    '---',
                    f'{subtotal:.2f}',
                    f'{iva:.2f}',
                    f'{total:.2f}',
                ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Ventas'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('sale_report')
        return context
