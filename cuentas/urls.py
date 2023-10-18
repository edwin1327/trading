from django.urls import path
from . import views


urlpatterns = [
    path('cuentas_usuario/', views.cuentas_usuario, name='cuentas_usuario'),
    path('crear_cuenta/', views.crear_cuenta, name='crear_cuenta'),
    path('eliminar_cuenta/<int:cuenta_id>/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('editar_cuenta/<int:cuenta_id>/', views.editar_cuenta, name='editar_cuenta'),  # Nueva URL
    path('estrategias/', views.estrategias, name='estrategias'),
    path('operar-metatrader/<int:cuenta_id>/', views.operar_metatrader, name='operar_metatrader'),
    path('crear_estrategia/', views.crear_estrategia, name='crear_estrategia'),
    path('cambiar_estado_estrategia/', views.cambiar_estado_estrategia, name='cambiar_estado_estrategia'),
    path('ejecutar_codigo_python/<int:estrategia_id>/', views.ejecutar_codigo_python, name='ejecutar_codigo_python'),
]