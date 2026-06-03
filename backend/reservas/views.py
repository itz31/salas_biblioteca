import json
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from salas.models import Sala
from salas.views import date_for_day, marcar_bloque_por_fecha, parse_range
from usuarios.models import Usuario

from .models import HistorialReserva, Reserva


def perfil_por_nombre(nombre):
    return Usuario.objects.filter(first_name=nombre).first()


def tabla_reservas_html(reservas):
    if not reservas:
        return '<tr><td colspan="4" class="text-center p-4">No tienes reservas activas.</td></tr>'

    filas = []
    for reserva in reservas:
        filas.append(
            f'''
            <tr class="border-b border-slate-100 hover:bg-slate-50 transition" data-id="{reserva.external_id or reserva.pk}">
              <td class="p-3 text-slate-700">{reserva.sala.nombre}</td>
              <td class="p-3 text-slate-600">{reserva.fecha}</td>
              <td class="p-3 text-slate-600">{reserva.hora_inicio.strftime('%H:%M')} - {reserva.hora_fin.strftime('%H:%M')}</td>
            </tr>
            '''
        )
    return ''.join(filas)


def tabla_historial_html(historial):
    if not historial:
        return ''

    filas = []
    for item in historial:
        if item.reserva:
            sala_nombre = item.reserva.sala.nombre
            fecha = item.reserva.fecha
            hora = f"{item.reserva.hora_inicio.strftime('%H:%M')} - {item.reserva.hora_fin.strftime('%H:%M')}"
        else:
            sala_nombre = item.detalle or ''
            fecha = ''
            hora = ''

        filas.append(
            f'''
            <tr class="border-b border-slate-100 hover:bg-slate-50 transition">
              <td class="p-3 text-slate-700">{sala_nombre}</td>
              <td class="p-3 text-slate-600">{fecha}</td>
              <td class="p-3 text-slate-600">{hora}</td>
            </tr>
            '''
        )
    return ''.join(filas)


@csrf_exempt
def reservas_html(request, param):
    if request.method == 'GET':
        usuario = perfil_por_nombre(param)
        if not usuario:
            return JsonResponse({'html': '<tr><td colspan="4" class="text-center p-4">No tienes reservas activas.</td></tr>'})

        reservas = Reserva.objects.filter(usuario=usuario).select_related('sala').order_by('-creada_en')
        return JsonResponse({'html': tabla_reservas_html(reservas)})

    if request.method == 'DELETE':
        reserva = Reserva.objects.filter(external_id=param).select_related('sala').first()
        if not reserva:
            return JsonResponse({'mensaje': 'Reserva no encontrada.'}, status=404)

        marcar_bloque_por_fecha(reserva.sala, reserva.fecha, reserva.hora_inicio.strftime('%H:%M'), reservado=False)
        HistorialReserva.objects.create(
            usuario=reserva.usuario,
            reserva=reserva,
            accion=HistorialReserva.Accion.ELIMINADA,
            detalle=reserva.sala.nombre,
        )
        reserva.delete()
        return JsonResponse({'mensaje': f'exito eliminacion reserva id {param}'})

    return JsonResponse({'mensaje': 'Método no permitido.'}, status=405)


def reservas_all_html(request):
    if request.method != 'GET':
        return JsonResponse({'mensaje': 'Método no permitido.'}, status=405)

    reservas = Reserva.objects.select_related('sala', 'usuario').order_by('-creada_en')
    return JsonResponse({'html': tabla_reservas_html(reservas)})


def historial_html(request, param):
    if request.method != 'GET':
        return JsonResponse({'html': ''})

    usuario = perfil_por_nombre(param)
    if not usuario:
        return JsonResponse({'html': ''})

    historial = HistorialReserva.objects.filter(usuario=usuario).select_related('reserva', 'reserva__sala').order_by('-creado_en')
    return JsonResponse({'html': tabla_historial_html(historial)})


@csrf_exempt
def crear_reserva(request):
    if request.method != 'POST':
        return JsonResponse({'mensaje': 'Método no permitido.'}, status=405)

    datos = json.loads(request.body or '{}')
    nombre_usuario = datos.get('nombreUsuario')
    sala_nombre = datos.get('sala')
    fecha_value = datos.get('fecha')
    hora_value = datos.get('hora') or ''
    external_id = datos.get('id') or f"res-{int(datetime.now().timestamp() * 1000)}"

    usuario = perfil_por_nombre(nombre_usuario)
    sala = Sala.objects.filter(nombre=sala_nombre).first()

    if not usuario or not sala:
        return JsonResponse({'mensaje': 'Faltan datos de la reserva.'}, status=400)

    fecha = date_for_day(fecha_value)
    hora_inicio, hora_fin = parse_range(hora_value)
    if not fecha or not hora_inicio or not hora_fin:
        return JsonResponse({'mensaje': 'Faltan datos de la reserva.'}, status=400)

    if Reserva.objects.filter(sala=sala, fecha=fecha, hora_inicio=hora_inicio, estado=Reserva.Estado.ACTIVA).exists():
        return JsonResponse({'mensaje': 'Ya existe una reserva para ese horario.'}, status=409)

    reserva = Reserva.objects.create(
        external_id=external_id,
        usuario=usuario,
        sala=sala,
        fecha=fecha,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        estado=Reserva.Estado.ACTIVA,
    )

    marcar_bloque_por_fecha(sala, fecha, hora_inicio.strftime('%H:%M'), reservado=True)
    HistorialReserva.objects.create(
        usuario=usuario,
        reserva=reserva,
        accion=HistorialReserva.Accion.CREADA,
        detalle=sala.nombre,
    )
    return JsonResponse({'mensaje': 'Reserva creada con éxito'}, status=201)


eliminar_reserva = reservas_html
