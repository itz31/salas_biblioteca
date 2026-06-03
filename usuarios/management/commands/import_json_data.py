from datetime import datetime
import json
from pathlib import Path

from django.core.management.base import BaseCommand

from reservas.models import HistorialReserva, Reserva
from salas.models import Sala
from usuarios.models import Usuario


class Command(BaseCommand):
    help = 'Importa los datos existentes del backend JSON al proyecto Django.'

    def add_arguments(self, parser):
        parser.add_argument(
            'archivo_json',
            nargs='?',
            default=None,
            help='Ruta opcional a un JSON consolidado con usuarios, salas, reservas e historial.',
        )

    def handle(self, *args, **options):
        root_dir = Path(__file__).resolve().parents[3]
        archivo_json = options.get('archivo_json')

        if archivo_json:
            archivo_path = Path(archivo_json)
            if not archivo_path.is_absolute():
                archivo_path = root_dir / archivo_path
            if not archivo_path.exists():
                raise FileNotFoundError(f'No existe el archivo JSON: {archivo_path}')

            data = json.loads(archivo_path.read_text(encoding='utf-8'))
            self.importar_usuarios(data.get('usuarios', data))
            self.importar_salas(data.get('salas', data))
            self.importar_reservas(data.get('reservas', []))
            self.importar_historial(data.get('historial', []))
        else:
            legacy_data_dir = root_dir / 'Taller antiguo (sin django y eso eliminar dsps)' / 'salas_biblioteca-main' / 'backend' / 'data'
            current_data_dir = root_dir / 'backend' / 'data'
            data_dir = legacy_data_dir if legacy_data_dir.exists() else current_data_dir

            self.importar_usuarios(data_dir / 'perfiles.json')
            self.importar_salas(data_dir / 'salas.json')
            self.importar_reservas(data_dir / 'reservas.json')
            self.importar_historial(data_dir / 'historial.json')
        self.crear_admin_por_defecto()

        self.stdout.write(self.style.SUCCESS('Datos importados correctamente.'))

    def importar_usuarios(self, file_path):
        if isinstance(file_path, (str, Path)):
            file_path = Path(file_path)
            if not file_path.exists():
                return
            data = json.loads(file_path.read_text(encoding='utf-8'))
        else:
            data = file_path

        if not isinstance(data, dict):
            return

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
        if isinstance(file_path, (str, Path)):
            file_path = Path(file_path)
            if not file_path.exists():
                return
            data = json.loads(file_path.read_text(encoding='utf-8'))
        else:
            data = file_path

        if not isinstance(data, dict):
            return

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
                    'disponibilidad': sala_data.get('disponibilidad', []),
                    'activa': True,
                },
            )

    def importar_reservas(self, file_path):
        if isinstance(file_path, (str, Path)):
            file_path = Path(file_path)
            if not file_path.exists():
                return
            data = json.loads(file_path.read_text(encoding='utf-8'))
        else:
            data = file_path

        if not isinstance(data, list):
            return

        for reserva in data:
            usuario = Usuario.objects.filter(first_name=reserva.get('nombreUsuario')).first()
            sala = Sala.objects.filter(nombre=reserva.get('sala')).first()
            if not usuario or not sala:
                continue

            fecha = self.parse_date(reserva.get('fecha'))
            hora_inicio, hora_fin = self.parse_range(reserva.get('hora', '00:00 - 00:00'))
            if not fecha or not hora_inicio or not hora_fin:
                continue

            external_id = str(reserva.get('id') or f'import-{usuario.id}-{sala.id}-{fecha}-{hora_inicio}')
            reserva_obj = Reserva.objects.filter(external_id=external_id).first()
            if not reserva_obj:
                reserva_obj = Reserva.objects.filter(
                    usuario=usuario,
                    sala=sala,
                    fecha=fecha,
                    hora_inicio=hora_inicio,
                ).first()

            if reserva_obj:
                reserva_obj.external_id = external_id
                reserva_obj.usuario = usuario
                reserva_obj.sala = sala
                reserva_obj.fecha = fecha
                reserva_obj.hora_inicio = hora_inicio
                reserva_obj.hora_fin = hora_fin
                reserva_obj.estado = Reserva.Estado.ACTIVA
                reserva_obj.save()
            else:
                reserva_obj = Reserva.objects.create(
                    external_id=external_id,
                    usuario=usuario,
                    sala=sala,
                    fecha=fecha,
                    hora_inicio=hora_inicio,
                    hora_fin=hora_fin,
                    estado=Reserva.Estado.ACTIVA,
                )
            self.marcar_bloque(sala, fecha, hora_inicio)

    def importar_historial(self, file_path):
        if isinstance(file_path, (str, Path)):
            file_path = Path(file_path)
            if not file_path.exists():
                return
            data = json.loads(file_path.read_text(encoding='utf-8'))
        else:
            data = file_path

        if not isinstance(data, list):
            return

        for registro in data:
            usuario = Usuario.objects.filter(first_name=registro.get('nombreUsuario')).first()
            if not usuario:
                continue

            sala = Sala.objects.filter(nombre=registro.get('sala')).first()
            reserva = None
            if sala:
                fecha = self.parse_date(registro.get('fecha'))
                hora_inicio, _ = self.parse_range(registro.get('hora', '00:00 - 00:00'))
                if registro.get('id'):
                    reserva = Reserva.objects.filter(external_id=str(registro.get('id'))).first()
                if not reserva and fecha and hora_inicio:
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

    @staticmethod
    def marcar_bloque(sala, fecha, hora_inicio):
        from salas.views import marcar_bloque_por_fecha

        marcar_bloque_por_fecha(sala, fecha, hora_inicio.strftime('%H:%M'), reservado=True)

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
        dias_fijos = {
            'lunes': '2026-06-01',
            'martes': '2026-06-02',
            'miercoles': '2026-06-03',
            'miércoles': '2026-06-03',
            'jueves': '2026-06-04',
            'viernes': '2026-06-05',
        }
        valor_normalizado = str(value).strip().lower()
        if valor_normalizado in dias_fijos:
            value = dias_fijos[valor_normalizado]
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
