from django.contrib import admin
from .models import Reserva, Historial


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'sala', 'fecha', 'hora', 'estado']
    list_filter = ['estado', 'fecha']
    search_fields = ['usuario__nombre', 'sala__numero']


@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'sala', 'fecha', 'hora', 'accion', 'created_at']
    list_filter = ['accion']
    search_fields = ['usuario__nombre']
