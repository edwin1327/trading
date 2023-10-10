from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.
# ==================== Vista Home ===========================

@login_required
def home(request):
    return render(request, 'home.html')


# ==================== Función de Logout ===========================
def salir(request):
    logout(request)
    return redirect('/')