from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PQRForm, GestionarPQRForm
from .models import peticion
from django.contrib.admin.views.decorators import staff_member_required
from datetime import datetime
from django.db.models import Q

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
            return redirect('pqr_list') 
    else:
        form = PQRForm()
    return render(request, 'crear_pqr.html', {'form': form})

# ================== Formulario detalle PQR usuarios ==========================================
@login_required
def ver_detalle_pqr(request, pqr_id):
    pqr = get_object_or_404(peticion, id=pqr_id, user=request.user)
    return render(request, 'ver_detalle_pqr.html', {'pqr': pqr})


# ========================== Gestión PQR Empleados Listado ==========================================

# Define una función para verificar si un usuario es staff
def es_staff(user):
    return user.is_staff

@login_required
@user_passes_test(es_staff)
def pqr_asignadas(request):
    pqr_list = peticion.objects.filter(Q(empleado_asignado=request.user) & ~Q(estado='Cerrado'))
    return render(request, 'pqr_asignadas.html', {'pqr_list': pqr_list})

# ========================== Gestión PQR Empleados ==========================================

def gestionar_pqr(request, pqr_id):
    pqr = get_object_or_404(peticion, pk=pqr_id)
    
    if request.method == 'POST':
        form = GestionarPQRForm(request.POST, instance=pqr)
        if form.is_valid():
            if 'cerrar_peticion' in request.POST and form.cleaned_data.get('descripcion_cierre'):
                pqr.estado = 'Cerrado'
                pqr.fecha_hora_cierre = datetime.now()
            elif 'asignar_peticion' in request.POST and form.cleaned_data.get('empleado_asignado') and form.cleaned_data.get('comentario_asignacion'):
                pqr.estado = 'Asignado'
                pqr.empleado_asignado = form.cleaned_data['empleado_asignado']
            pqr.save()
            form = GestionarPQRForm(instance=pqr)
            return redirect('pqr_asignadas') 
    else:
        form = GestionarPQRForm(instance=pqr)

    return render(request, 'pqr_gestionar.html', {'form': form, 'pqr': pqr})