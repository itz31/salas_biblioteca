from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class UsuarioManager(UserManager):
	def create_user(self, correo, password=None, **extra_fields):
		if not correo:
			raise ValueError('El correo es obligatorio.')

		correo = self.normalize_email(correo)
		extra_fields.setdefault('username', extra_fields.get('username') or correo)

		user = self.model(correo=correo, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, correo, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('tipo_usuario', Usuario.TipoUsuario.FUNCIONARIO)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('El superusuario debe tener is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('El superusuario debe tener is_superuser=True.')

		return self.create_user(correo, password, **extra_fields)


class Usuario(AbstractUser):
	class TipoUsuario(models.TextChoices):
		ESTUDIANTE = 'estudiante', 'Estudiante'
		FUNCIONARIO = 'funcionario', 'Funcionario'

	correo = models.EmailField(unique=True)
	tipo_usuario = models.CharField(
		max_length=20,
		choices=TipoUsuario.choices,
		default=TipoUsuario.ESTUDIANTE,
	)

	objects = UsuarioManager()

	USERNAME_FIELD = 'correo'
	REQUIRED_FIELDS = ['username']

	def __str__(self):
		return f'{self.get_full_name() or self.username} <{self.correo}>'
