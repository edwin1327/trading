from django.shortcuts import render
from .models import Cuenta  # Importa el modelo de Cuenta
from django.contrib.auth.decorators import login_required

# ====================== Lista de Cuentas Trading del Usuario =================
@login_required
def cuentas_usuario(request):
    cuentas = Cuenta.objects.filter(user=request.user)
    return render(request, 'cuentas_usuario.html', {'cuentas': cuentas})

