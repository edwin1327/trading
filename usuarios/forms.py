from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User

class CustomUserCreationForm(UserCreationForm):
    #adress = forms.CharField(max_length=100, required=False)  # Campo para la dirección
    #city = forms.CharField(max_length=50, required=False)     # Campo para la ciudad
    #country = forms.CharField(max_length=50, required=False)  # Campo para el país

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'adress', 'city', 'country']