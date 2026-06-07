from django.contrib import admin
from .models import Sala, Disponibilidad


class DisponibilidadInline(admin.TabularInline):
    model = Disponibilidad
    extra = 0


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ['numero', 'piso', 'capacidad', 'pizarra', 'television']
    list_filter = ['piso']
    inlines = [DisponibilidadInline]


@admin.register(Disponibilidad)
class DisponibilidadAdmin(admin.ModelAdmin):
    list_display = ['sala', 'bloque', 'dia', 'disponible']
    list_filter = ['dia', 'disponible']
