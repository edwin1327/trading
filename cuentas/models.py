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
        return self.name_broker
    
class Estrategia(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    descripcion = models.TextField()
    codigo_python = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
    

class Crear_Estrategia(models.Model):
    ONEMINUTE = "1M"
    FIVEMINUTES = "5M"
    FIFTEENMINUTES = "15M"
    THIRTYMINUTES = "30M"
    ONEHOUR = "1H"
    FOURHOURS = "4H"
    ONEDAY = "1D"
    TIMEFRAME_STRATEGY = [
        (ONEMINUTE, "1 Minuto"),
        (FIVEMINUTES, "5 Minutos"),
        (FIFTEENMINUTES, "15 Minutos"),
        (THIRTYMINUTES, "30 Minutos"),
        (ONEHOUR, "1 Hora"),
        (FOURHOURS, "4 Horas"),
        (ONEDAY, "1 Día"),
    ]

    id_cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE) # Relación con la cuenta Activa
    nombre_estrategia = models.CharField(max_length=50)
    id_estrategia = models.ForeignKey(Estrategia, on_delete=models.CASCADE)
    divisa = models.CharField(max_length=10, blank=False, null=False)
    timeframe = models.CharField(max_length=3, blank=False, null=False, choices=TIMEFRAME_STRATEGY, default=ONEDAY)
    estado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre_estrategia

