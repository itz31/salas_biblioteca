from rest_framework import viewsets
from .models import Sala, Disponibilidad
from .serializers import SalaListSerializer, SalaDetailSerializer, DisponibilidadSerializer


class SalasViewSet(viewsets.ModelViewSet):
    """
    GET    /api/salas/          → lista de salas
    GET    /api/salas/<numero>/ → detalle con disponibilidades
    POST   /api/salas/          → crear sala
    PUT    /api/salas/<numero>/ → actualizar sala
    DELETE /api/salas/<numero>/ → eliminar sala
    """
    queryset = Sala.objects.all()
    lookup_field = 'numero'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SalaDetailSerializer
        return SalaListSerializer


class DisponibilidadViewSet(viewsets.ModelViewSet):
    """
    GET /api/salas/disponibilidades/?sala=<numero> → disponibilidades de una sala
    """
    queryset = Disponibilidad.objects.all()
    serializer_class = DisponibilidadSerializer

    def get_queryset(self):
        queryset = Disponibilidad.objects.all()
        sala_numero = self.request.query_params.get('sala')
        if sala_numero:
            queryset = queryset.filter(sala__numero=sala_numero)
        return queryset
