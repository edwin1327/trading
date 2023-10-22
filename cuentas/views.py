import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from threading import Thread
from .forms import AgregarCuentaForm, AgregarEstrategiaForm, EditarCuentaForm
from .models import Cuenta, Estrategia, Crear_Estrategia
from schedule import every, run_pending, cancel_job
import pytz, time
from collections import defaultdict
from functools import partial

# ============== Entornos Globales ==================================
# Diccionario para realizar un seguimiento de las tareas programadas
tareas_programadas = {}

# Objeto datetime con información de zona horaria
timezone = pytz.timezone("UTC")
now = datetime.now(timezone)

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

# ====================== Editar Cuentas Trading del Usuario =================

@login_required
def editar_cuenta(request, cuenta_id):
    cuenta = get_object_or_404(Cuenta, id=cuenta_id)

    if request.method == 'POST':
        form = EditarCuentaForm(request.POST, instance=cuenta)
        if form.is_valid():
            form.save()
            return redirect('cuentas_usuario')

    else:
        form = EditarCuentaForm(instance=cuenta)

    return render(request, 'editar_cuenta.html', {'form': form, 'cuenta': cuenta})

# ====================== Eliminar Cuentas Trading del Usuario =================

@login_required
def eliminar_cuenta(request, cuenta_id):
    cuenta = get_object_or_404(Cuenta, id=cuenta_id)

    if request.method == 'POST':
        # Elimina la cuenta
        cuenta.delete()
        return redirect('cuentas_usuario')

    return render(request, 'eliminar_cuenta.html', {'cuenta': cuenta})

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

            # Obtener estrategias asociadas a la cuenta actual
            estrategias_usuario = Crear_Estrategia.objects.filter(id_cuenta_id=cuenta_id)


            # Agregar el saldo y el DataFrame al contexto
            context = {
                'account_info_df': account_info_df.to_html(classes='table table-bordered table-hover'),
                'saldo': saldo,
                'estrategias_usuario': estrategias_usuario,
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

# ======================= Cambiar estado de estrategia de Trading ====================

@csrf_exempt
def cambiar_estado_estrategia(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        estrategia_id = request.POST.get('estrategia_id')
        try:
            estrategia = Crear_Estrategia.objects.get(id=estrategia_id)
            estado_anterior = estrategia.estado
            estrategia.estado = not estrategia.estado  # Cambia el estado
            estrategia.save()

            # Si el estado cambió a "Inactivo," detener la tarea programada
            if estado_anterior and not estrategia.estado:
                detener_tarea_programada(estrategia_id)
            else:
                # Define una función parcial que fija el parámetro request
                partial_ejecutar_codigo_python = partial(ejecutar_codigo_python, request)
                ejecutar_codigo_python(partial_ejecutar_codigo_python, estrategia_id)

            return JsonResponse({'estado': estrategia.estado})
        except Crear_Estrategia.DoesNotExist:
            return JsonResponse({'error': 'Estrategia no encontrada'}, status=400)
    else:
        return JsonResponse({'error': 'Solicitud no válida'}, status=400)

# ======================= Ejecutar estrategia de Trading ====================

def ejecutar_codigo_python(request, estrategia_id):
    estrategia_usuario = Crear_Estrategia.objects.get(id=estrategia_id)
    estrategia = estrategia_usuario.id_estrategia
    # Define un diccionario para el entorno
    context = {}
    # El estado debe estar activo antes de ejecutar el código
    if estrategia_usuario.estado:
        try:
            # Definir los argumentos que se pasarán a la función
            divisa = estrategia_usuario.divisa
            timeframe = estrategia_usuario.timeframe
            # Ejecuta el código Python almacenado en el campo codigo_python
            exec(estrategia.codigo_python, context)

            # Llama a la función con los argumentos
            context['implementar_estrategia'](divisa, timeframe)
            mensaje = "Código ejecutado exitosamente."

            # Calcular el tiempo de espera antes de la próxima ejecución
            intervalo = 60  # Predeterminado a 1 minuto
            if estrategia_usuario.timeframe == '5M':
                intervalo = 300  # 5 minutos
            elif estrategia_usuario.timeframe == '15M':
                intervalo = 900  # 15 minutos
            elif estrategia_usuario.timeframe == '30M':
                intervalo = 1800  # 30 minutos
            elif estrategia_usuario.timeframe == '1H':
                intervalo = 3600  # 1 hora
            elif estrategia_usuario.timeframe == '4H':
                intervalo = 14400  # 4 horas
            elif estrategia_usuario.timeframe == '1D':
                intervalo = 86400  # 1 día

            # Define una función parcial que fija el parámetro request
            partial_ejecutar_codigo_python = partial(ejecutar_codigo_python, request)

            # Programar la próxima ejecución
            estrategia_id = estrategia_usuario.id
            tarea = every(intervalo).seconds.do(partial_ejecutar_codigo_python, estrategia_id)
            tareas_programadas[estrategia_id] = tarea
            cantidad = 0
            for tarea in tareas_programadas:
                cantidad += 1
                print(f"{cantidad}. Tarea: {tarea}")
            
            # Inicia el hilo para ejecutar tareas programadas en segundo plano
            t = Thread(target=ejecutar_tareas_programadas)
            t.daemon = True
            t.start()

            estrategia_usuario.ultima_ejecucion = datetime.now(timezone)
            estrategia_usuario.save()
        except Exception as e:
            mensaje = f"Error al ejecutar el código: {str(e)}"
    else:
        mensaje = "La estrategia está inactiva."

    return JsonResponse({'mensaje': mensaje})



# ======================= Funciones tareas segundo plano ====================
   
# Función para ejecutar tareas programadas
def ejecutar_tareas_programadas():
    while True:
        run_pending()
        time.sleep(60)  # Espera 60 segundos antes de verificar nuevamente las tareas
        

# Función para detener una tarea programada
def detener_tarea_programada(estrategia_id):
    estrategia_id = int(estrategia_id)
    if estrategia_id in tareas_programadas:
        cancelar_tarea = tareas_programadas[estrategia_id]
        #primera_tarea = conjunto_de_tareas.pop()  # Remueve y obtiene la primera tarea
        cancel_job(cancelar_tarea)
        del tareas_programadas[estrategia_id]
        print(f"Tarea programada para {estrategia_id} fue cancelada y eliminada")
    else:
        print(f"No se encontró tarea programada para {estrategia_id}")
