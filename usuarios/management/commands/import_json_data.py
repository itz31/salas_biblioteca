from datetime import datetime
import json
from pathlib import Path

from django.core.management.base import BaseCommand

from reservas.models import HistorialReserva, Reserva
from salas.models import Sala
from usuarios.models import Usuario


class Command(BaseCommand):
    help = 'Importa los datos existentes del backend JSON al proyecto Django.'

    def handle(self, *args, **options):
        root_dir = Path(__file__).resolve().parents[4]
        data_dir = root_dir / 'backend' / 'data'

        self.importar_usuarios(data_dir / 'perfiles.json')
        self.importar_salas(data_dir / 'salas.json')
        self.importar_reservas(data_dir / 'reservas.json')
        self.importar_historial(data_dir / 'historial.json')
        self.crear_admin_por_defecto()

        self.stdout.write(self.style.SUCCESS('Datos importados correctamente.'))

    def importar_usuarios(self, file_path):
        if not file_path.exists():
            return

        data = json.loads(file_path.read_text(encoding='utf-8'))
        for grupo in ('estudiantes', 'funcionarios'):
            for perfil in data.get(grupo, []):
                usuario, _ = Usuario.objects.update_or_create(
                    correo=perfil['correo'],
                    defaults={
                        'username': perfil.get('correo', perfil['correo']),
                        'first_name': perfil.get('nombre', ''),
                        'tipo_usuario': perfil.get('tipo', 'estudiante'),
                        'is_active': True,
                    },
                )
                usuario.set_password(perfil.get('password', 'Cambiar123'))
                usuario.save(update_fields=['password'])

    def importar_salas(self, file_path):
        if not file_path.exists():
            return

        data = json.loads(file_path.read_text(encoding='utf-8'))
        for key, sala_data in data.items():
            numero = str(sala_data.get('numero', key))
            codigo = f'S-{numero.zfill(3)}'
            Sala.objects.update_or_create(
                codigo=codigo,
                defaults={
                    'nombre': f'Sala {numero}',
                    'piso': sala_data.get('piso', 'Piso 1'),
                    'capacidad': int(sala_data.get('capacidad', 0)),
                    'sillas': int(sala_data.get('sillas', 0)),
                    'pizarra': sala_data.get('pizarra', ''),
                    'multimedia': sala_data.get('television', '').lower() != 'no tiene',
                    'entorno': sala_data.get('vista', ''),
                    'activa': True,
                },
            )

    def importar_reservas(self, file_path):
        if not file_path.exists():
            return

        data = json.loads(file_path.read_text(encoding='utf-8'))
        for reserva in data:
            usuario = Usuario.objects.filter(first_name=reserva.get('nombreUsuario')).first()
            sala = Sala.objects.filter(nombre=reserva.get('sala')).first()
            if not usuario or not sala:
                continue

            fecha = self.parse_date(reserva.get('fecha'))
            hora_inicio, hora_fin = self.parse_range(reserva.get('hora', '00:00 - 00:00'))
            if not fecha or not hora_inicio or not hora_fin:
                continue

            Reserva.objects.update_or_create(
                usuario=usuario,
                sala=sala,
                fecha=fecha,
                hora_inicio=hora_inicio,
                defaults={
                    'hora_fin': hora_fin,
                    'estado': Reserva.Estado.ACTIVA,
                },
            )

    def importar_historial(self, file_path):
        if not file_path.exists():
            return

        data = json.loads(file_path.read_text(encoding='utf-8'))
        for registro in data:
            usuario = Usuario.objects.filter(first_name=registro.get('nombreUsuario')).first()
            if not usuario:
                continue

            sala = Sala.objects.filter(nombre=registro.get('sala')).first()
            reserva = None
            if sala:
                fecha = self.parse_date(registro.get('fecha'))
                hora_inicio, _ = self.parse_range(registro.get('hora', '00:00 - 00:00'))
                reserva = Reserva.objects.filter(
                    usuario=usuario,
                    sala=sala,
                    fecha=fecha,
                    hora_inicio=hora_inicio,
                ).first()

            HistorialReserva.objects.update_or_create(
                usuario=usuario,
                reserva=reserva,
                accion=HistorialReserva.Accion.CREADA,
                detalle=registro.get('sala', ''),
                defaults={},
            )

    def crear_admin_por_defecto(self):
        correo_admin = 'admin@admin.com'
        password_admin = 'admin'

        admin_usuario, _ = Usuario.objects.update_or_create(
            correo=correo_admin,
            defaults={
                'username': 'admin',
                'first_name': 'Admin',
                'last_name': 'Sistema',
                'tipo_usuario': Usuario.TipoUsuario.FUNCIONARIO,
                'is_active': True,
                'is_staff': True,
                'is_superuser': True,
            },
        )
        admin_usuario.set_password(password_admin)
        admin_usuario.save()

    @staticmethod
    def parse_date(value):
        if not value:
            return None
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            return None

    @staticmethod
    def parse_time(value):
        if not value:
            return None
        for fmt in ('%H:%M', '%H:%M:%S'):
            try:
                return datetime.strptime(value, fmt).time()
            except ValueError:
                continue
        return None

    def parse_range(self, value):
        if not value or '-' not in value:
            return None, None
        inicio, fin = [parte.strip() for parte in value.split('-', 1)]
        return self.parse_time(inicio), self.parse_time(fin)
