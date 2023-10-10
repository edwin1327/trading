from django.urls import path
from .views import home, salir


urlpatterns = [
    path('', home, name='home'),
    path('logout/', salir, name='salir'),
]