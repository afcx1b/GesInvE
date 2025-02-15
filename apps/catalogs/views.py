from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelformset_factory
from .forms import OfferForm, OfferDetailForm, OrderForm, OrderDetailForm, BannerForm, CatalogForm, CatalogProductForm
from .models import Offer, OfferDetail, Order, Banner, OrderDetail, Catalog, CatalogProduct
from apps.products.models import Product
from apps.categories.models import Category

def catalog_by_category(request, id):
    category = get_object_or_404(Category, idCategory=id)
    allowed_categories = ["CAPILAR", "CORPORAL", "FACIAL", "HOGAR", "LABIOS", "MANOS", "MPIGMENTACION", "OJOS", "PIES", "SEXSHOP", "UÑAS"]
    products = Product.objects.filter(idCategory=category, idCategory__parent__isnull=True, idCategory__category__in=allowed_categories)
    return render(request, 'catalogs/catalog_by_category.html', {'category': category, 'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, idProduct=id)
    return render(request, 'catalogs/product_detail.html', {'product': product})

# Vistas para Ofertas
def offer_list(request):
    offers = Offer.objects.all()
    return render(request, 'catalogs/offer_list.html', {'offers': offers})

def create_offer(request):
    OfferDetailFormSet = modelformset_factory(OfferDetail, form=OfferDetailForm, extra=1)
    if request.method == 'POST':
        offer_form = OfferForm(request.POST)
        offer_detail_formset = OfferDetailFormSet(request.POST)
        if offer_form.is_valid() and offer_detail_formset.is_valid():
            offer = offer_form.save()
            offer_details = offer_detail_formset.save(commit=False)
            for offer_detail in offer_details:
                offer_detail.offer = offer
                offer_detail.save()
            return redirect('offer_list')
    else:
        offer_form = OfferForm()
        offer_detail_formset = OfferDetailFormSet()
    return render(request, 'catalogs/offer_create.html', {'offer_form': offer_form, 'offer_detail_formset': offer_detail_formset})

def edit_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    OfferDetailFormSet = modelformset_factory(OfferDetail, form=OfferDetailForm, extra=1)
    if request.method == 'POST':
        offer_form = OfferForm(request.POST, instance=offer)
        offer_detail_formset = OfferDetailFormSet(request.POST)
        if offer_form.is_valid() and offer_detail_formset.is_valid():
            offer = offer_form.save()
            offer_details = offer_detail_formset.save(commit=False)
            for offer_detail in offer_details:
                offer_detail.offer = offer
                offer_detail.save()
            return redirect('offer_list')
    else:
        offer_form = OfferForm(instance=offer)
        offer_detail_formset = OfferDetailFormSet(queryset=OfferDetail.objects.filter(offer=offer))
    return render(request, 'catalogs/offer_edit.html', {'offer_form': offer_form, 'offer_detail_formset': offer_detail_formset})

def delete_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    if request.method == 'POST':
        offer.delete()
        return redirect('offer_list')
    return render(request, 'catalogs/offer_confirm_delete.html', {'offer': offer})

# Vistas para Órdenes
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'catalogs/order_list.html', {'orders': orders})

def create_order(request):
    OrderDetailFormSet = modelformset_factory(OrderDetail, form=OrderDetailForm, extra=1)
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        order_detail_formset = OrderDetailFormSet(request.POST)
        if order_form.is_valid() and order_detail_formset.is_valid():
            order = order_form.save()
            order_details = order_detail_formset.save(commit=False)
            for order_detail in order_details:
                order_detail.order = order
                order_detail.save()
            return redirect('order_list')
    else:
        order_form = OrderForm()
        order_detail_formset = OrderDetailFormSet()
    return render(request, 'catalogs/order_create.html', {'order_form': order_form, 'order_detail_formset': order_detail_formset})

def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    OrderDetailFormSet = modelformset_factory(OrderDetail, form=OrderDetailForm, extra=1)
    if request.method == 'POST':
        order_form = OrderForm(request.POST, instance=order)
        order_detail_formset = OrderDetailFormSet(request.POST)
        if order_form.is_valid() and order_detail_formset.is_valid():
            order = order_form.save()
            order_details = order_detail_formset.save(commit=False)
            for order_detail in order_details:
                order_detail.order = order
                order_detail.save()
            return redirect('order_list')
    else:
        order_form = OrderForm(instance=order)
        order_detail_formset = OrderDetailFormSet(queryset=OrderDetail.objects.filter(order=order))
    return render(request, 'catalogs/order_edit.html', {'order_form': order_form, 'order_detail_formset': order_detail_formset})

def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'catalogs/order_confirm_delete.html', {'order': order})

# Vistas para Banners
def banner_list(request):
    banners = Banner.objects.all()
    return render(request, 'catalogs/banner_list.html', {'banners': banners})

def create_banner(request):
    if request.method == 'POST':
        banner_form = BannerForm(request.POST, request.FILES)
        if banner_form.is_valid():
            banner_form.save()
            return redirect('banner_list')
    else:
        banner_form = BannerForm()
    return render(request, 'catalogs/banner_create.html', {'banner_form': banner_form})

def edit_banner(request, banner_id):
    banner = get_object_or_404(Banner, id=banner_id)
    if request.method == 'POST':
        banner_form = BannerForm(request.POST, request.FILES, instance=banner)
        if banner_form.is_valid():
            banner_form.save()
            return redirect('banner_list')
    else:
        banner_form = BannerForm(instance=banner)
    return render(request, 'catalogs/banner_edit.html', {'banner_form': banner_form})

def delete_banner(request, banner_id):
    banner = get_object_or_404(Banner, id=banner_id)
    if request.method == 'POST':
        banner.delete()
        return redirect('banner_list')
    return render(request, 'catalogs/banner_confirm_delete.html', {'banner': banner})

# Vistas para Catálogos
def catalog_list(request):
    catalogs = Catalog.objects.all()
    return render(request, 'catalogs/catalog_list.html', {'catalogs': catalogs})

def create_catalog(request):
    if request.method == 'POST':
        catalog_form = CatalogForm(request.POST, request.FILES)
        if catalog_form.is_valid():
            catalog_form.save()
            return redirect('catalog_list')
        else:
            print(catalog_form.errors)  # Agrega esta línea para imprimir los errores del formulario
    else:
        catalog_form = CatalogForm()
    return render(request, 'catalogs/catalog_create.html', {'catalog_form': catalog_form})

def edit_catalog(request, catalog_id):
    catalog = get_object_or_404(Catalog, id=catalog_id)
    if request.method == 'POST':
        catalog_form = CatalogForm(request.POST, request.FILES, instance=catalog)
        if catalog_form.is_valid():
            catalog_form.save()
            return redirect('catalog_list')
    else:
        catalog_form = CatalogForm(instance=catalog)
    return render(request, 'catalogs/catalog_edit.html', {'catalog_form': catalog_form})

def delete_catalog(request, catalog_id):
    catalog = get_object_or_404(Catalog, id=catalog_id)
    if request.method == 'POST':
        catalog.delete()
        return redirect('catalog_list')
    return render(request, 'catalogs/catalog_confirm_delete.html', {'catalog': catalog})

# Vistas para Productos de Catálogos
def catalog_product_list(request):
    catalog_products = CatalogProduct.objects.all()
    return render(request, 'catalogs/catalog_product_list.html', {'catalog_products': catalog_products})

def create_catalog_product(request):
    if request.method == 'POST':
        catalog_product_form = CatalogProductForm(request.POST)
        if catalog_product_form.is_valid():
            catalog_product_form.save()
            return redirect('catalog_product_list')
    else:
        catalog_product_form = CatalogProductForm()
    return render(request, 'catalogs/catalog_product_create.html', {'catalog_product_form': catalog_product_form})

def edit_catalog_product(request, catalog_product_id):
    catalog_product = get_object_or_404(CatalogProduct, id=catalog_product_id)
    if request.method == 'POST':
        catalog_product_form = CatalogProductForm(request.POST, instance=catalog_product)
        if catalog_product_form.is_valid():
            catalog_product_form.save()
            return redirect('catalog_product_list')
    else:
        catalog_product_form = CatalogProductForm(instance=catalog_product)
    return render(request, 'catalogs/catalog_product_edit.html', {'catalog_product_form': catalog_product_form})

def delete_catalog_product(request, catalog_product_id):
    catalog_product = get_object_or_404(CatalogProduct, id=catalog_product_id)
    if request.method == 'POST':
        catalog_product.delete()
        return redirect('catalog_product_list')
    return render(request, 'catalogs/catalog_product_confirm_delete.html', {'catalog_product': catalog_product})