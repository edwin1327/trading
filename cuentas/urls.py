from django.urls import path
from . import views


urlpatterns = [
    path('cuentas_usuario/', views.cuentas_usuario, name='cuentas_usuario'),
    path('crear_cuenta/', views.crear_cuenta, name='crear_cuenta'),
    path('estrategias/', views.estrategias, name='estrategias'),
    path('operar-metatrader/', views.operar_metatrader, name='operar_metatrader'),
]