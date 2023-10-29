from django import forms
from .models import peticion
from usuarios.models import User

class PQRForm(forms.ModelForm):
    class Meta:
        model = peticion
        fields = ['tipo_solicitud', 'descripcion']


class GestionarPQRForm(forms.ModelForm):
    empleado_asignado = forms.ModelChoiceField(queryset=User.objects.filter(is_staff=True))
    descripcion_cierre = forms.CharField(widget=forms.Textarea, required=False)
    comentario_asignacion = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = peticion
        fields = ['empleado_asignado', 'descripcion_cierre', 'comentario_asignacion']