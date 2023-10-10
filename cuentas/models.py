from django.db import models
from usuarios.models import User

# Create your models here.
class Cuenta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con el usuario
    name_broker = models.CharField(max_length=20, blank=False, null=False)
    numero_cuenta = models.IntegerField()
    pass_server = models.CharField(max_length=20, blank=False, null=False)
    server = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return self.user.username  # Representación legible en el administrador de Django
