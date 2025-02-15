from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Gasto
from .forms import GastoForm
 
@login_required
def lista_gastos(request):
    gastos = Gasto.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'gastos/gasto_lista.html', {'gastos': gastos})

@login_required
def agregar_gasto(request):
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            gasto = form.save(commit=False)
            gasto.usuario = request.user
            gasto.save()
            return redirect('lista_gastos')
    else:
        form = GastoForm()
    return render(request, 'gastos/gasto_form.html', {'form': form})

@login_required
def editar_gasto(request, gasto_id):
    gasto = get_object_or_404(Gasto, id=gasto_id, usuario=request.user)
    if request.method == 'POST':
        form = GastoForm(request.POST, instance=gasto)
        if form.is_valid():
            form.save()
            return redirect('lista_gastos')
    else:
        form = GastoForm(instance=gasto)
    return render(request, 'gastos/gasto_form.html', {'form': form})

@login_required
def eliminar_gasto(request, gasto_id):
    gasto = get_object_or_404(Gasto, id=gasto_id, usuario=request.user)
    if request.method == 'POST':
        gasto.delete()
        return redirect('lista_gastos')
    return render(request, 'gastos/gasto_confirm_delete.html', {'gasto': gasto})
