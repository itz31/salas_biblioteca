from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Usuario
from .serializers import UsuarioSerializer, UsuarioDetailSerializer

DOMINIOS = {
    '@alumnos.ucn.cl': ('estudiante', 'E'),
    '@funcionario.ucn.cl': ('funcionario', 'F'),
}


def detectar_tipo(correo):
    """Devuelve (tipo, prefijo) según el dominio del correo, o (None, None)."""
    correo = correo.lower()
    for dominio, (tipo, prefijo) in DOMINIOS.items():
        if correo.endswith(dominio):
            return tipo, prefijo
    return None, None


def generar_id(prefijo):
    """Genera el siguiente ID disponible, ej: E004."""
    count = Usuario.objects.filter(id_usuario__startswith=prefijo).count() + 1
    return f"{prefijo}{str(count).zfill(3)}"


class LoginView(APIView):
    """POST /api/usuarios/login/"""

    def post(self, request):
        correo = request.data.get('correo', '').strip().lower()
        password = request.data.get('password', '')

        if not correo or not password:
            return Response(
                {'error': 'Correo y contraseña son requeridos'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            usuario = Usuario.objects.get(correo=correo)
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Usuario no encontrado'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not usuario.check_password(password):
            return Response(
                {'error': 'Contraseña incorrecta'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            {'mensaje': 'Login exitoso', 'usuario': UsuarioSerializer(usuario).data},
            status=status.HTTP_200_OK,
        )


class RegisterView(APIView):
    """POST /api/usuarios/register/"""

    def post(self, request):
        nombre = request.data.get('nombre', '').strip()
        correo = request.data.get('correo', '').strip().lower()
        password = request.data.get('password', '')

        if not all([nombre, correo, password]):
            return Response(
                {'error': 'Nombre, correo y contraseña son requeridos'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        tipo, prefijo = detectar_tipo(correo)
        if not tipo:
            return Response(
                {'error': 'El correo debe terminar en @alumnos.ucn.cl o @funcionario.ucn.cl'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Usuario.objects.filter(correo=correo).exists():
            return Response(
                {'error': 'El correo ya está registrado'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        usuario = Usuario(
            id_usuario=generar_id(prefijo),
            nombre=nombre,
            correo=correo,
            tipo=tipo,
        )
        usuario.set_password(password)
        usuario.save()

        return Response(
            {'mensaje': 'Usuario creado exitosamente', 'usuario': UsuarioSerializer(usuario).data},
            status=status.HTTP_201_CREATED,
        )


class UsuariosViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/usuarios/  y  GET /api/usuarios/<id_usuario>/"""
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    lookup_field = 'id_usuario'
