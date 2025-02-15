from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from apps.catalogs.models import Catalog
from apps.products.models import Product



def index(request):
    catalogs = Catalog.objects.all()
    products = Product.objects.all()
    return render(request, 'index.html', {'catalogs': catalogs, 'products': products})


def catalog_detail(request, id):
    catalog = get_object_or_404(Catalog, id=id)
    products = catalog.product_set.all()
    return render(request, 'catalog_detail.html', {'catalog': catalog, 'products': products})


class IndexView(TemplateView):
    template_name = 'index.html'











