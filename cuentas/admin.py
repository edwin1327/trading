from django.contrib import admin
from .models import Cuenta, Estrategia

# Crear las clases para personalizar el Admin
class EstrategiaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'descripcion')
    list_filter = ('tipo',)  # Opcional, agrega un filtro por tipo
    search_fields = ('nombre',)  # Opcional, habilita la búsqueda por nombre


# Register your models here.
admin.site.register(Cuenta)
admin.site.register(Estrategia, EstrategiaAdmin)