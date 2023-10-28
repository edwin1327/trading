from django import forms
from .models import peticion
from usuarios.models import User

class PQRForm(forms.ModelForm):
    class Meta:
        model = peticion
        fields = ['tipo_solicitud', 'descripcion']
