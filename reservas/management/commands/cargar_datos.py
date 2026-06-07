import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import datetime

from usuario.models import Usuario
from salas.models import Sala, Disponibilidad
from reservas.models import Reserva, Historial


class Command(BaseCommand):
    help = 'Carga datos iniciales desde los archivos JSON en data/'

    def add_arguments(self, parser):
        parser.add_argument(
            '--data-dir',
            type=str,
            default='data',
            help='Directorio con los archivos JSON (por defecto: data/)',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        data_dir = Path(options['data_dir'])
        self._cargar_usuarios(data_dir)
        self._cargar_salas(data_dir)
        self._cargar_reservas(data_dir)
        self.stdout.write(self.style.SUCCESS('✓ Datos cargados correctamente'))

    def _cargar_usuarios(self, data_dir):
        archivo = data_dir / 'perfiles.json'
        if not archivo.exists():
            self.stdout.write(self.style.WARNING(f'No encontrado: {archivo}'))
            return

        datos = json.loads(archivo.read_text(encoding='utf-8'))
        creados = 0
        for grupo in ('estudiantes', 'funcionarios'):
            for perfil in datos.get(grupo, []):
                usuario, nuevo = Usuario.objects.get_or_create(
                    id_usuario=perfil['id'],
                    defaults={
                        'nombre': perfil['nombre'],
                        'correo': perfil['correo'],
                        'tipo': perfil['tipo'],
                    },
                )
                if nuevo:
                    usuario.set_password(perfil['password'])
                    usuario.save()
                    creados += 1
        self.stdout.write(self.style.SUCCESS(f'  ✓ {creados} usuarios cargados'))

    def _cargar_salas(self, data_dir):
        archivo = data_dir / 'salas.json'
        if not archivo.exists():
            self.stdout.write(self.style.WARNING(f'No encontrado: {archivo}'))
            return

        datos = json.loads(archivo.read_text(encoding='utf-8'))
        salas_creadas = 0
        disps_creadas = 0

        for sala_data in datos.values():
            sala, nuevo = Sala.objects.get_or_create(
                numero=sala_data['numero'],
                defaults={
                    'piso': sala_data['piso'],
                    'imagen': sala_data.get('imagen', ''),
                    'sillas': int(sala_data.get('sillas', 0)),
                    'capacidad': int(sala_data.get('capacidad', 0)),
                    'pizarra': sala_data['pizarra'],
                    'television': sala_data['television'],
                    'vista': sala_data['vista'],
                },
            )
            if nuevo:
                salas_creadas += 1

            for bloque_data in sala_data.get('disponibilidad', []):
                bloque = bloque_data['bloque']
                for dia in ('lunes', 'martes', 'miercoles', 'jueves', 'viernes'):
                    _, nuevo = Disponibilidad.objects.get_or_create(
                        sala=sala,
                        bloque=bloque,
                        dia=dia,
                        defaults={'disponible': bloque_data.get(dia, True)},
                    )
                    if nuevo:
                        disps_creadas += 1

        self.stdout.write(
            self.style.SUCCESS(f'  ✓ {salas_creadas} salas y {disps_creadas} disponibilidades cargadas')
        )

    def _cargar_reservas(self, data_dir):
        archivo = data_dir / 'reservas.json'
        if not archivo.exists():
            self.stdout.write(self.style.WARNING(f'No encontrado: {archivo}'))
            return

        datos = json.loads(archivo.read_text(encoding='utf-8'))
        creadas = 0

        for r in datos:
            usuario = Usuario.objects.filter(nombre__icontains=r['nombreUsuario']).first()
            sala = Sala.objects.filter(numero=r['sala']).first()
            if not usuario or not sala:
                continue

            fecha_str = r.get('fecha', '')
            try:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                fecha = datetime.now().date()

            reserva, nuevo = Reserva.objects.get_or_create(
                usuario=usuario, sala=sala, fecha=fecha, hora=r['hora'],
                defaults={'estado': 'confirmada'},
            )
            if nuevo:
                creadas += 1
                Historial.objects.get_or_create(
                    usuario=usuario, sala=sala, fecha=fecha, hora=r['hora'],
                    defaults={'accion': 'reserva'},
                )

        self.stdout.write(self.style.SUCCESS(f'  ✓ {creadas} reservas cargadas'))
