from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Usuario(models.Model):
    TIPO_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('funcionario', 'Funcionario'),
    ]

    id_usuario = models.CharField(max_length=10, unique=True, primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['correo']),
            models.Index(fields=['tipo']),
        ]
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.nombre} ({self.id_usuario})"
