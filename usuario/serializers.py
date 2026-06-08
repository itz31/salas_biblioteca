from rest_framework import serializers
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id_usuario', 'nombre', 'correo', 'tipo', 'created_at']
        read_only_fields = ['id_usuario', 'created_at']


class UsuarioDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id_usuario', 'nombre', 'correo', 'tipo', 'created_at', 'updated_at']
        read_only_fields = ['id_usuario', 'created_at', 'updated_at']
