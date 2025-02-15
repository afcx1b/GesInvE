from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Proveedor, Compra, DetalleCompra
from .forms import ProveedorForm, CompraForm, DetalleCompraForm
from apps.kardex.models import Kardex
from apps.inventory.models import Inventario
from apps.kardex.models import Costo

 
@login_required
def lista_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'compras/proveedor_lista.html', {'proveedores': proveedores})

@login_required
def agregar_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'compras/proveedor_form.html', {'form': form})

@login_required
def lista_compras(request):
    compras = Compra.objects.all()
    return render(request, 'compras/compra_lista.html', {'compras': compras})


@login_required
def crear_compra(request):
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.usuario = request.user
            compra.save()
            
            # Registrar en Kardex
            for detalle in compra.detalles.all():
                Kardex.objects.create(
                    producto=detalle.articulo,
                    cantidad=detalle.cantidad,
                    tipo_movimiento='entrada',
                    fecha=compra.fecha
                )
                
                # Registrar en Inventario
                inventario, created = Inventario.objects.get_or_create(producto=detalle.articulo)
                inventario.cantidad += detalle.cantidad
                inventario.save()
                
                # Registrar en Costo
                Costo.objects.create(
                    producto=detalle.articulo,
                    costo=detalle.costo,
                    fecha=compra.fecha
                ) 
            
            return redirect('detalle_compra', compra.id)
    else:
        form = CompraForm()
    return render(request, 'compras/compra_detalle.html', {'form': form})

@login_required
def detalle_compra(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    detalles = compra.detalles.all()

    if request.method == 'POST':
        form = DetalleCompraForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.compra = compra
            detalle.save()
            return redirect('detalle_compra', compra_id=compra.id)
    else:
        form = DetalleCompraForm()

    return render(request, 'compras/compra_detalle.html', {'compra': compra, 'detalles': detalles, 'form': form})
