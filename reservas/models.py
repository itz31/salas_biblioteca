from django.db import models
from usuario.models import Usuario
from salas.models import Sala, Disponibilidad


class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reservas')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='reservas')
    disponibilidad = models.ForeignKey(
        Disponibilidad, on_delete=models.CASCADE,
        related_name='reservas', null=True, blank=True,
    )
    fecha = models.DateField()
    hora = models.CharField(max_length=20)   # ej: "08:00 - 09:30"
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='confirmada')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('usuario', 'sala', 'fecha', 'hora')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['usuario', 'fecha']),
            models.Index(fields=['sala', 'fecha']),
        ]
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f"{self.usuario.nombre} - Sala {self.sala.numero} - {self.fecha}"


class Historial(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='historial')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.CharField(max_length=20)
    accion = models.CharField(max_length=50)   # 'reserva' o 'cancelacion'
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['usuario', 'created_at'])]
        verbose_name = 'Historial'
        verbose_name_plural = 'Historial'

    def __str__(self):
        return f"{self.usuario.nombre} - {self.accion} - {self.fecha}"
