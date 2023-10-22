from django import forms
from .models import Cuenta, Crear_Estrategia

class AgregarCuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['name_broker', 'numero_cuenta', 'pass_server', 'server']

class EditarCuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['name_broker', 'numero_cuenta', 'pass_server', 'server']  # Lista de campos que deseas editar

class AgregarEstrategiaForm(forms.ModelForm):
    class Meta:
        model = Crear_Estrategia
        fields = ['nombre_estrategia', 'id_estrategia', 'divisa', 'timeframe']

class EditarEstrategiaForm(forms.ModelForm):
    class Meta:
        model = Crear_Estrategia
        fields = ['nombre_estrategia', 'id_estrategia', 'divisa', 'timeframe']