from rest_framework import viewsets
from salas.models import Disponibilidad
from .models import Reserva, Historial
from .serializers import ReservaSerializer, HistorialSerializer


class ReservasViewSet(viewsets.ModelViewSet):
    """
    GET    /api/reservas/?usuario=<id>  → reservas de un usuario
    GET    /api/reservas/?sala=<numero> → reservas de una sala
    POST   /api/reservas/               → crear reserva
    DELETE /api/reservas/<id>/          → cancelar reserva
    """
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def get_queryset(self):
        queryset = Reserva.objects.all()
        usuario_id = self.request.query_params.get('usuario')
        sala_numero = self.request.query_params.get('sala')
        if usuario_id:
            queryset = queryset.filter(usuario__id_usuario=usuario_id)
        if sala_numero:
            queryset = queryset.filter(sala__numero=sala_numero)
        return queryset

    def perform_create(self, serializer):
        reserva = serializer.save()
        Historial.objects.create(
            usuario=reserva.usuario,
            sala=reserva.sala,
            fecha=reserva.fecha,
            hora=reserva.hora,
            accion='reserva',
        )
        Disponibilidad.objects.filter(
            sala=reserva.sala,
            bloque=reserva.hora,
        ).update(disponible=False)

    def perform_destroy(self, instance):
        Historial.objects.create(
            usuario=instance.usuario,
            sala=instance.sala,
            fecha=instance.fecha,
            hora=instance.hora,
            accion='cancelacion',
        )
        Disponibilidad.objects.filter(
            sala=instance.sala,
            bloque=instance.hora,
        ).update(disponible=True)
        instance.delete()


class HistorialViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/reservas/historial/?usuario=<id> → historial de un usuario
    """
    queryset = Historial.objects.all()
    serializer_class = HistorialSerializer

    def get_queryset(self):
        queryset = Historial.objects.all()
        usuario_id = self.request.query_params.get('usuario')
        if usuario_id:
            queryset = queryset.filter(usuario__id_usuario=usuario_id)
        return queryset
