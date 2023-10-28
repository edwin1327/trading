from django import forms
from .models import peticion

class PQRForm(forms.ModelForm):
    class Meta:
        model = peticion
        fields = ['tipo_solicitud', 'descripcion']
        