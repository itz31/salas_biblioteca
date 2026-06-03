from django.db import models


class Sala(models.Model):
	class Piso(models.TextChoices):
		PRIMERO = 'Piso 1', 'Piso 1'
		MENOS_UNO = 'Piso -1', 'Piso -1'
		SEGUNDO = 'Piso 2', 'Piso 2'

	codigo = models.CharField(max_length=10, unique=True)
	nombre = models.CharField(max_length=100)
	piso = models.CharField(max_length=20, choices=Piso.choices)
	capacidad = models.PositiveIntegerField()
	sillas = models.PositiveIntegerField()
	pizarra = models.CharField(max_length=30)
	multimedia = models.BooleanField(default=False)
	entorno = models.CharField(max_length=100, blank=True)
	activa = models.BooleanField(default=True)

	class Meta:
		ordering = ['codigo']

	def __str__(self):
		return f'{self.codigo} - {self.nombre}'
