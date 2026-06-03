from django.conf import settings
from django.db import models

from salas.models import Sala


class Reserva(models.Model):
	class Estado(models.TextChoices):
		ACTIVA = 'activa', 'Activa'
		CANCELADA = 'cancelada', 'Cancelada'
		FINALIZADA = 'finalizada', 'Finalizada'

	usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservas')
	sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='reservas')
	fecha = models.DateField()
	hora_inicio = models.TimeField()
	hora_fin = models.TimeField()
	estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ACTIVA)
	creada_en = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-creada_en']
		constraints = [
			models.UniqueConstraint(
				fields=['sala', 'fecha', 'hora_inicio'],
				name='uniq_reserva_por_sala_fecha_inicio',
			)
		]

	def __str__(self):
		return f'{self.usuario} - {self.sala} - {self.fecha} {self.hora_inicio}'


class HistorialReserva(models.Model):
	class Accion(models.TextChoices):
		CREADA = 'creada', 'Creada'
		CANCELADA = 'cancelada', 'Cancelada'
		ELIMINADA = 'eliminada', 'Eliminada'

	usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='historial_reservas')
	reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='historial', null=True, blank=True)
	accion = models.CharField(max_length=20, choices=Accion.choices)
	detalle = models.CharField(max_length=255, blank=True)
	creado_en = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-creado_en']

	def __str__(self):
		return f'{self.usuario} - {self.accion}'
