import json

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Usuario


def perfil_response(user):
	tipo = 'administrador' if user.is_superuser else user.tipo_usuario
	return {
		'id': user.id,
		'nombre': user.first_name or user.username,
		'correo': user.correo,
		'tipo': tipo,
	}


@csrf_exempt
def api_login(request):
	if request.method != 'POST':
		return JsonResponse({'mensaje': 'Método no permitido.'}, status=405)

	data = json.loads(request.body or '{}')
	correo = (data.get('correo') or '').strip().lower()
	password = data.get('password') or ''

	user = authenticate(request, username=correo, password=password)
	if user is None:
		return JsonResponse({'mensaje': 'Correo o contraseña incorrectos.'}, status=401)

	login(request, user)
	return JsonResponse({'perfil': perfil_response(user)})


@csrf_exempt
def api_register(request):
	if request.method != 'POST':
		return JsonResponse({'mensaje': 'Método no permitido.'}, status=405)

	data = json.loads(request.body or '{}')
	nombre = (data.get('nombre') or '').strip()
	correo = (data.get('correo') or '').strip().lower()
	password = data.get('password') or ''
	tipo_usuario = (data.get('tipo_usuario') or Usuario.TipoUsuario.ESTUDIANTE).strip().lower()

	if not nombre or not correo or not password:
		return JsonResponse({'mensaje': 'Debes completar nombre, correo y contraseña.'}, status=400)
	if Usuario.objects.filter(correo=correo).exists():
		return JsonResponse({'mensaje': 'Ese correo ya está registrado.'}, status=409)
	if not correo.endswith('@alumnos.ucn.cl') and not correo.endswith('@funcionario.ucn.cl'):
		return JsonResponse({'mensaje': 'El correo debe terminar en @alumnos.ucn.cl o @funcionario.ucn.cl.'}, status=400)
	if correo.endswith('@funcionario.ucn.cl'):
		tipo_usuario = Usuario.TipoUsuario.FUNCIONARIO

	usuario = Usuario.objects.create_user(
		correo=correo,
		password=password,
		username=correo,
		first_name=nombre,
		tipo_usuario=tipo_usuario,
	)
	login(request, usuario)
	return JsonResponse({'perfil': perfil_response(usuario)}, status=201)
