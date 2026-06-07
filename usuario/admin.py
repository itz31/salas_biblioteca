from django.contrib import admin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['id_usuario', 'nombre', 'correo', 'tipo', 'created_at']
    list_filter = ['tipo']
    search_fields = ['nombre', 'correo']
