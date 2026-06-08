from rest_framework import serializers
from .models import Sala, Disponibilidad


class DisponibilidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disponibilidad
        fields = ['id', 'sala', 'bloque', 'dia', 'disponible', 'created_at']
        read_only_fields = ['id', 'created_at']


class SalaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ['numero', 'piso', 'capacidad', 'pizarra', 'television', 'imagen']


class SalaDetailSerializer(serializers.ModelSerializer):
    disponibilidades = DisponibilidadSerializer(many=True, read_only=True)

    class Meta:
        model = Sala
        fields = [
            'numero', 'piso', 'imagen', 'sillas', 'capacidad',
            'pizarra', 'television', 'vista', 'disponibilidades', 'created_at',
        ]
        read_only_fields = ['numero', 'created_at']
