# Sistema de Reservas de Salas de Biblioteca

Proyecto reorganizado para funcionar con una arquitectura clara:

- `backend/`: proyecto Django, apps, datos y configuración.
- `frontend/`: plantillas HTML y assets estáticos.
- `manage.py`: entrada principal desde la raíz.
- `datos_iniciales.json`: datos iniciales consolidados para carga rápida.

## Qué incluye ahora

- Django 6 con SQLite como backend.
- Frontend heredado conservado en `frontend/`.
- Usuario personalizado con login por correo.
- Modelos de salas, reservas e historial.
- Comando de importación de JSON compatible con el nuevo layout.
- Acceso al panel de admin Django.

## Estructura actual

- `backend/config/`: configuración del proyecto Django.
- `backend/usuarios/`: app de usuario y comando `import_json_data`.
- `backend/salas/`: app de salas.
- `backend/reservas/`: app de reservas e historial.
- `backend/data/`: JSON antiguos de datos iniciales.
- `frontend/templates/`: plantillas HTML.
- `frontend/static/`: CSS y JavaScript.
- `datos_iniciales.json`: seed consolidado en la raíz.

## Cómo iniciar el proyecto

### Opción recomendada

Ejecuta `iniciar.bat` desde la raíz del proyecto.

El script realiza:

1. Activación o creación del entorno virtual.
2. Instalación de dependencias.
3. Aplicación de migraciones Django.
4. Importación de datos iniciales.
5. Inicio del servidor Django.
6. Apertura del navegador en `http://127.0.0.1:8000`.

### Opción manual

Desde la raíz del proyecto:

```bat
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py import_json_data
python manage.py runserver
```

Abre luego:

```text
http://127.0.0.1:8000
```

## Cómo cargar datos iniciales

### Importar desde `datos_iniciales.json`

```bat
python manage.py import_json_data datos_iniciales.json
```

### Importar desde los archivos antiguos de backend

```bat
python manage.py import_json_data
```

El comando leerá automáticamente los JSON en `backend/data/` si no se pasa archivo.

## Usuario administrador

- Correo: `admin@admin.com`
- Contraseña: `admin`

## Vistas principales

- `/login.html` - página de login/registro.
- `/mapa.html` - vista principal de salas.
- `/detalleSalas.html?id=<ID>` - detalle de sala.
- `/usuario.html` - perfil/usuario.
- `/admin/` - panel de administración Django.

## Qué falta implementar para el Taller 2

1. Pulir el frontend para que el UI siga el requerimiento exacto del taller.
2. Completar validaciones de formularios y mensajes de error en reservas.
3. Probar los flujos de reserva, edición/cancelación y visualización de historial.
4. Añadir pruebas automáticas para modelos y API si se desea.
5. Ajustar la experiencia de usuario en caso de errores o reservas inválidas.

## Archivos clave

- `backend/config/settings.py`
- `backend/usuarios/management/commands/import_json_data.py`
- `backend/usuarios/models.py`
- `backend/salas/models.py`
- `backend/reservas/models.py`
- `frontend/templates/`
- `frontend/static/`
- `datos_iniciales.json`
- `DOCUMENTACION.md`

## Nota

El proyecto está enfocado en mantener solo las carpetas `frontend/` y `backend/` junto a los archivos necesarios en la raíz. El viejo backend Node/Express y los assets no usados fueron removidos para simplificar el repositorio.