from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import PQRForm
from .models import peticion

# ======================= Listado de PQR's ===============================================

@login_required
def pqr_list(request):
    pqr_list = peticion.objects.filter(user=request.user)
    return render(request, 'pqr_list.html', {'pqr_list': pqr_list})

# =================== Formulario para crear PQR's ===========================================

@login_required
def crear_pqr(request):
    if request.method == 'POST':
        form = PQRForm(request.POST)
        if form.is_valid():
            pqr = form.save(commit=False)
            pqr.user = request.user
            pqr.save()
            return redirect('pqr_list')  # Redirige a la lista de PQR u otra vista de tu elección
    else:
        form = PQRForm()
    return render(request, 'crear_pqr.html', {'form': form})