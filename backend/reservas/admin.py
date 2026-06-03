from django.contrib import admin

from .models import HistorialReserva, Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'sala', 'fecha', 'hora_inicio', 'hora_fin', 'estado', 'creada_en')
	list_filter = ('estado', 'fecha', 'sala')
	search_fields = ('usuario__correo', 'usuario__username', 'sala__codigo', 'sala__nombre')


@admin.register(HistorialReserva)
class HistorialReservaAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'reserva', 'accion', 'creado_en')
	list_filter = ('accion', 'creado_en')
	search_fields = ('usuario__correo', 'detalle')
