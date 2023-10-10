from django.db import models
from usuarios.models import User

# Create your models here.
class Cuenta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario
    numero_cuenta = models.IntegerField()
    pass_server = models.CharField(max_length=255)
    server = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username  # Representación legible en el administrador de Django
