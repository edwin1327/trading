from django.urls import path
from . import views


urlpatterns = [
    path('cuentas_usuario/', views.cuentas_usuario, name='cuentas_usuario'),
    path('crear_cuenta/', views.crear_cuenta, name='crear_cuenta'),
    path('eliminar_cuenta/<int:cuenta_id>/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('estrategias/', views.estrategias, name='estrategias'),
    path('operar-metatrader/<int:cuenta_id>/', views.operar_metatrader, name='operar_metatrader'),
    path('crear_estrategia/', views.crear_estrategia, name='crear_estrategia'),
]