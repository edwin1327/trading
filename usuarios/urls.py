from django.urls import path
from .views import home, salir, register


urlpatterns = [
    path('', home, name='home'),
    path('logout/', salir, name='salir'),
    path('register/', register, name='register'),
]