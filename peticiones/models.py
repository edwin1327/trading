from django.db import models
from usuarios.models import User

class peticion(models.Model):
    TIPOS_PQR = (
        ('Petición', 'Petición'),
        ('Queja', 'Queja'),
        ('Reclamo', 'Reclamo'),
    )

    ESTADOS_PQR = (
        ('Radicado', 'Radicado'),
        ('Asignado', 'Asignado'),
        ('En Trámite', 'En Trámite'),
        ('Cerrado', 'Cerrado')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pqr_usuario')
    tipo_solicitud = models.CharField(max_length=8, choices=TIPOS_PQR)
    descripcion = models.TextField()
    fecha_hora_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADOS_PQR, default='Radicado')
    empleado_asignado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pqr_empleado', default=1)
    fecha_hora_cierre = models.DateTimeField(null=True, blank=True)
    descripcion_cierre = models.TextField(null=True, blank=True)
    comentario_asignacion = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_tipo_solicitud_display()} - {self.id}"

class AsignacionPQR(models.Model):
    pqr = models.ForeignKey(peticion, on_delete=models.CASCADE)
    empleado_asignado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asignacion_pqr_empleado')
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    comentario_asignacion = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Asignación de PQR {self.pqr_id} a {self.empleado_asignado.username}"
