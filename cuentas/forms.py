from django import forms
from .models import Cuenta

class AgregarCuentaForm(forms.ModelForm):
    class Meta:
        model = Cuenta
        fields = ['name_broker', 'numero_cuenta', 'pass_server', 'server']
