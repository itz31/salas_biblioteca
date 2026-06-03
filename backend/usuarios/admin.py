from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
	model = Usuario
	ordering = ('correo',)
	list_display = ('correo', 'username', 'first_name', 'last_name', 'tipo_usuario', 'is_staff')
	fieldsets = UserAdmin.fieldsets + (("Datos del sistema", {"fields": ("correo", "tipo_usuario")} ),)
	add_fieldsets = UserAdmin.add_fieldsets + (("Datos del sistema", {"fields": ("correo", "tipo_usuario")} ),)
	search_fields = ('correo', 'username', 'first_name', 'last_name')
