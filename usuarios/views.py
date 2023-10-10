from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm

# Create your views here.
# ==================== Vista Home ===========================

@login_required
def home(request):
    return render(request, 'home.html')


# ==================== Función de Logout ===========================
def salir(request):
    logout(request)
    return redirect('/')

# ==================== Vista Registro Usuario ===========================

def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            return redirect('home')
    return render(request, 'registration/register.html', data)
