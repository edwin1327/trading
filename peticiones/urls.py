from django.urls import path
from . import views


urlpatterns = [
    path('crear_pqr/', views.crear_pqr, name='crear_pqr'),
    path('pqr_list/', views.pqr_list, name='pqr_list'),
    path('ver_detalle_pqr/<int:pqr_id>/', views.ver_detalle_pqr, name='ver_detalle_pqr'),
    path('pqr_asignadas/', views.pqr_asignadas, name='pqr_asignadas'),
    path('gestionar_pqr/<int:pqr_id>/', views.gestionar_pqr, name='gestionar_pqr'),
]