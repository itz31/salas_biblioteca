import json
from datetime import date, datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from reservas.models import Reserva

from .models import Sala


DAY_ORDER = [
    ('lunes', 'Lunes'),
    ('martes', 'Martes'),
    ('miercoles', 'Miércoles'),
    ('jueves', 'Jueves'),
    ('viernes', 'Viernes'),
]

DAY_TO_DATE = {
    'lunes': date(2026, 6, 1),
    'martes': date(2026, 6, 2),
    'miercoles': date(2026, 6, 3),
    'miércoles': date(2026, 6, 3),
    'jueves': date(2026, 6, 4),
    'viernes': date(2026, 6, 5),
}


def normalizar_dia(value):
    if not value:
        return ''
    return (
        str(value)
        .strip()
        .lower()
        .replace('á', 'a')
        .replace('é', 'e')
        .replace('í', 'i')
        .replace('ó', 'o')
        .replace('ú', 'u')
    )


def parse_time(value):
    if not value:
        return None
    for fmt in ('%H:%M', '%H:%M:%S'):
        try:
            return datetime.strptime(value, fmt).time()
        except ValueError:
            continue
    return None


def parse_range(value):
    if not value or '-' not in value:
        return None, None
    inicio, fin = [parte.strip() for parte in value.split('-', 1)]
    return parse_time(inicio), parse_time(fin)


def date_for_day(value):
    if isinstance(value, date):
        return value

    value_norm = normalizar_dia(value)
    if value_norm in DAY_TO_DATE:
        return DAY_TO_DATE[value_norm]

    try:
        return datetime.strptime(str(value), '%Y-%m-%d').date()
    except ValueError:
        return None


def day_key_from_date(value):
    if not value:
        return None

    weekday_map = {
        0: 'lunes',
        1: 'martes',
        2: 'miercoles',
        3: 'jueves',
        4: 'viernes',
    }
    return weekday_map.get(value.weekday())


def actualizar_disponibilidad(sala, dia, hora_inicio, reservado=True):
    dia_key = normalizar_dia(dia)
    if dia_key not in dict(DAY_ORDER):
        return

    bloques = sala.disponibilidad or []
    for bloque in bloques:
        if bloque.get('bloque', '').startswith(hora_inicio):
            bloque[dia_key] = not reservado
            break

    sala.disponibilidad = bloques
    sala.save(update_fields=['disponibilidad'])


def marcar_bloque_por_fecha(sala, fecha_value, hora_inicio, reservado=True):
    fecha = date_for_day(fecha_value)
    if not fecha:
        return

    dia_key = day_key_from_date(fecha)
    if not dia_key:
        return

    actualizar_disponibilidad(sala, dia_key, hora_inicio, reservado=reservado)


def sala_a_dict(sala):
    horarios = []
    for bloque in sala.disponibilidad or []:
        hora_inicio, hora_fin = parse_range(bloque.get('bloque', ''))
        for dia_key, dia_nombre in DAY_ORDER:
            reservado_por_bloque = not bool(bloque.get(dia_key, True))
            reservado_por_reserva = False
            fecha_demo = DAY_TO_DATE.get(dia_key)

            if fecha_demo and hora_inicio:
                reservado_por_reserva = Reserva.objects.filter(
                    sala=sala,
                    fecha=fecha_demo,
                    hora_inicio=hora_inicio,
                    estado=Reserva.Estado.ACTIVA,
                ).exists()

            horarios.append({
                'dia': dia_nombre,
                'hora_inicio': hora_inicio.strftime('%H:%M') if hora_inicio else '',
                'hora_finalizacion': hora_fin.strftime('%H:%M') if hora_fin else '',
                'reservada': reservado_por_bloque or reservado_por_reserva,
            })

    return {
        'id': sala.codigo,
        'nombre': sala.nombre,
        'piso': sala.piso,
        'capacidad': sala.capacidad,
        'sillas': sala.sillas,
        'pizarra': sala.pizarra,
        'multimedia': sala.multimedia,
        'entorno': sala.entorno,
        'horarios': horarios,
    }


def salas_api(request):
    if request.method != 'GET':
        return JsonResponse({'mensaje': 'Método no permitido.'}, status=405)

    payload = [
        {'id': sala.codigo, 'nombre': sala.nombre}
        for sala in Sala.objects.filter(activa=True).order_by('codigo')
    ]
    return JsonResponse(payload, safe=False)


@csrf_exempt
def sala_detalle_api(request, param):
    if request.method == 'GET':
        codigo = param.split(',')[0]
        sala = Sala.objects.filter(codigo=codigo).first()
        if not sala:
            return JsonResponse([], safe=False)
        return JsonResponse([sala_a_dict(sala)], safe=False)

    if request.method == 'PUT':
        codigo, hora_inicio = param.split(',', 1)
        sala = Sala.objects.filter(codigo=codigo).first()
        if not sala:
            return JsonResponse({'mensaje': 'Sala no encontrada.'}, status=404)

        datos = json.loads(request.body or '{}')
        dia = datos.get('dia')
        actualizar_disponibilidad(sala, dia, hora_inicio, reservado=True)
        return JsonResponse({'mensaje': 'se ha reservado con exito'})

    return JsonResponse({'mensaje': 'Método no permitido.'}, status=405)


sala_reservar_api = sala_detalle_api
