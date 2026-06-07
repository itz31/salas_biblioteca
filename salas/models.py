from django.db import models


class Sala(models.Model):
    numero = models.CharField(max_length=10, unique=True, primary_key=True)
    piso = models.CharField(max_length=50)
    imagen = models.CharField(max_length=255, null=True, blank=True)
    sillas = models.IntegerField()
    capacidad = models.IntegerField()
    pizarra = models.CharField(max_length=50)
    television = models.CharField(max_length=50)
    vista = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['numero']
        indexes = [models.Index(fields=['piso'])]
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'

    def __str__(self):
        return f"Sala {self.numero} - {self.piso}"


class Disponibilidad(models.Model):
    DIAS_CHOICES = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
    ]

    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='disponibilidades')
    bloque = models.CharField(max_length=20)   # ej: "08:00 - 09:30"
    dia = models.CharField(max_length=20, choices=DIAS_CHOICES)
    disponible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sala', 'bloque', 'dia')
        ordering = ['dia', 'bloque']
        verbose_name = 'Disponibilidad'
        verbose_name_plural = 'Disponibilidades'

    def __str__(self):
        return f"{self.sala.numero} - {self.bloque} ({self.dia})"
