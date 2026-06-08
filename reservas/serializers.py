from rest_framework import serializers
from .models import Reserva, Historial


class ReservaSerializer(serializers.ModelSerializer):
    sala_numero = serializers.CharField(source='sala.numero', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)

    class Meta:
        model = Reserva
        fields = [
            'id', 'usuario', 'sala', 'sala_numero', 'usuario_nombre',
            'fecha', 'hora', 'estado', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class HistorialSerializer(serializers.ModelSerializer):
    sala_numero = serializers.CharField(source='sala.numero', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)

    class Meta:
        model = Historial
        fields = [
            'id', 'usuario', 'sala', 'sala_numero', 'usuario_nombre',
            'fecha', 'hora', 'accion', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']
