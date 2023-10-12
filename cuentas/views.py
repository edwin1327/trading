from django.shortcuts import render, redirect
from .forms import AgregarCuentaForm
from .models import Cuenta, Estrategia
from django.contrib.auth.decorators import login_required

# ====================== Lista de Cuentas Trading del Usuario =================
@login_required
def cuentas_usuario(request):
    cuentas = Cuenta.objects.filter(user=request.user)
    return render(request, 'cuentas_usuario.html', {'cuentas': cuentas})

# ====================== Crear Cuentas Trading del Usuario =================

@login_required
def crear_cuenta(request):
    if request.method == 'POST':
        form = AgregarCuentaForm(request.POST)
        if form.is_valid():
            # Guardar la cuenta en la base de datos
            nueva_cuenta = form.save(commit=False)
            nueva_cuenta.user = request.user # Asignar al usuario actual
            nueva_cuenta.save()
            return redirect('cuentas_usuario')  # Redirige a la lista de cuentas
    else:
        form = AgregarCuentaForm()
    return render(request, 'crear_cuenta.html', {'form': form})

# ====================== Lista de estrategias Trading disponibles =================

def estrategias(request):
    estrategias = Estrategia.objects.all()
    return render(request, 'estrategias.html', {'estrategias': estrategias})
