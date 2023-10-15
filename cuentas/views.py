import MetaTrader5 as mt5
import pandas as pd
from django.shortcuts import render, redirect
from .forms import AgregarCuentaForm, AgregarEstrategiaForm
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

@login_required
def estrategias(request):
    estrategias = Estrategia.objects.all()
    return render(request, 'estrategias.html', {'estrategias': estrategias})

# ====================== Lista de estrategias Trading disponibles =================

def operar_metatrader(request, cuenta_id):
    try:
        request.session['cuenta_id'] = cuenta_id
        # Obtén la cuenta basada en el cuenta_id
        datos_conexion = Cuenta.objects.get(id=cuenta_id)
        conexion_mt5 = {
            'path': 'C:\\Program Files\\RoboForex - MetaTrader 5\\terminal64.exe',
            'login': datos_conexion.numero_cuenta,
            'password': datos_conexion.pass_server,
            'server': datos_conexion.server,
            'timeout': 60000,
            'portable': False
        }

        if mt5.initialize(path=conexion_mt5['path'], login=conexion_mt5['login'], password=conexion_mt5['password'], server=conexion_mt5['server'], timeout=conexion_mt5['timeout'], portable=conexion_mt5['portable']):
            print("Conexión exitosa a plataforma MT5")

            # Obtener información de la cuenta
            account_info_dict = mt5.account_info()._asdict()
            account_info_df = pd.DataFrame(account_info_dict, index=[0])

            # Obtener el saldo de la cuenta
            saldo = account_info_dict.get('balance', 0)  # Obtener el saldo, 0 si no se encuentra

            # Agregar el saldo y el DataFrame al contexto
            context = {
                'account_info_df': account_info_df.to_html(classes='table table-bordered table-hover'),
                'saldo': saldo,
            }

        else:
            print(f"Ha ocurrido un problema en la iniciación: {mt5.last_error()}")

        return render(request, 'operaciones.html', context)
    except Cuenta.DoesNotExist:
        mensaje = "No se encontraron datos de conexión en la base de datos."
        print(mensaje)
    except Exception as e:
        mensaje = f"Error al abrir MetaTrader5: {str(e)}"
        print(mensaje)

    return render(request, 'operaciones.html', {'mensaje': mensaje}, cuenta_id)

# ======================= Formulario agregar estrategia de Trading ====================

@login_required
def crear_estrategia(request):
    if request.method == 'POST':
        form = AgregarEstrategiaForm(request.POST)
        if form.is_valid():
            nueva_estrategia = form.save(commit=False)
            # Recupera cuenta_id de la sesión
            cuenta_id = request.session.get('cuenta_id')
            # Asigna el valor de cuenta_id
            nueva_estrategia.id_cuenta_id = cuenta_id  # Asigna la cuenta correspondiente
            nueva_estrategia.save()
            return redirect('operar_metatrader', cuenta_id=cuenta_id)  # Redirige a la página de operaciones
    else:
        form = AgregarEstrategiaForm()
    return render(request, 'crear_estrategia.html', {'form': form})