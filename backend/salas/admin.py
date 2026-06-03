from django.contrib import admin

from .models import Sala


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
	list_display = ('codigo', 'nombre', 'piso', 'capacidad', 'sillas', 'multimedia', 'activa')
	search_fields = ('codigo', 'nombre', 'entorno')
	list_filter = ('piso', 'multimedia', 'activa')
