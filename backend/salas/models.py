from django.db import models


class Sala(models.Model):
	codigo = models.CharField(max_length=10, unique=True)
	nombre = models.CharField(max_length=100)
	piso = models.CharField(max_length=50)
	capacidad = models.PositiveIntegerField()
	sillas = models.PositiveIntegerField()
	pizarra = models.CharField(max_length=30)
	multimedia = models.BooleanField(default=False)
	entorno = models.CharField(max_length=100, blank=True)
	disponibilidad = models.JSONField(default=list, blank=True)
	activa = models.BooleanField(default=True)

	class Meta:
		ordering = ['codigo']

	def __str__(self):
		return f'{self.codigo} - {self.nombre}'
