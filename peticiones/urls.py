from django.urls import path
from . import views


urlpatterns = [
    path('crear_pqr/', views.crear_pqr, name='crear_pqr'),
    path('pqr_list/', views.pqr_list, name='pqr_list'),
]