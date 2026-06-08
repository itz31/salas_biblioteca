#!/usr/bin/env python
import os
import sys


def crear_superusuario_admin():
    try:
        import django
        django.setup()
        from django.contrib.auth import get_user_model

        User = get_user_model()
        admin_username = 'admin'
        admin_email = 'admin@example.com'
        admin_password = 'admin'

        usuario_admin = User.objects.filter(username=admin_username).first()
        if usuario_admin is None:
            User.objects.create_superuser(admin_username, admin_email, admin_password)
            print('Superusuario admin creado automáticamente.')
        else:
            if not usuario_admin.is_superuser or not usuario_admin.is_staff:
                usuario_admin.is_superuser = True
                usuario_admin.is_staff = True
                usuario_admin.save()
                print('Superusuario admin actualizado con privilegios de administrador.')
    except Exception:
        pass


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se pudo importar Django. ¿Está instalado?"
        ) from exc

    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        crear_superusuario_admin()

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
