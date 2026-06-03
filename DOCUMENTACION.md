# Documentación del proyecto

Este archivo describe estructura, archivos, funciones, rutas y flujos de importación.

## Raíz del proyecto

### `manage.py`
- Punto de entrada principal para Django.
- Inserta `backend/` en `sys.path` para que Django cargue las apps desde la nueva ubicación.
- Configura `DJANGO_SETTINGS_MODULE` como `config.settings`.
- Ejecuta comandos de Django como `migrate`, `runserver` y `import_json_data`.

### `datos_iniciales.json`
- JSON consolidado con usuarios, salas, reservas e historial.
- Se puede usar como entrada directa para `python manage.py import_json_data datos_iniciales.json`.
- Contiene los datos actuales del proyecto heredado.

## Carpeta `backend/config`

### `settings.py`
- Define `BASE_DIR` como `backend/config` y `ROOT_DIR` como la raíz del proyecto.
- Configura la base de datos SQLite en `db.sqlite3` en la raíz.
- Añade `frontend/templates` a `TEMPLATES['DIRS']` para que Django sirva las páginas HTML.
- Añade `frontend/static` a `STATICFILES_DIRS` para que Django sirva CSS y JS.
- Define `AUTH_USER_MODEL = 'usuarios.Usuario'` para usar el modelo personalizado.
- Configura URLs de login y redirect propios de Django.

### `urls.py`
- Mapea rutas públicas y API a funciones de vista.
- Importa vistas de:
  - `config.views` para páginas HTML.
  - `usuarios.views` para login y registro.
  - `salas.views` para lista y detalle de salas.
  - `reservas.views` para reservas e historial.
- Rutas clave:
  - `/` → `index`.
  - `/login.html` → formulario de login.
  - `/mapa.html` → mapa de salas.
  - `/detalleSalas.html` → detalle de sala.
  - `/usuario.html` → perfil/usuario.
  - `/api/login` → `api_login`.
  - `/api/register` → `api_register`.
  - `/salas` → `salas_api`.
  - `/salas/<param>` → `sala_detalle_api`.
  - `/reservas` → `crear_reserva`.
  - `/reservas/<param>` → `reservas_html` para ver o eliminar reservas.
  - `/historial/<param>` → historial del usuario.
  - `/admin/` → panel de administración estándar.

### `views.py`
- Sirve las páginas HTML estáticas con `render`.
- Cada función devuelve un template en `frontend/templates`.
- No usa datos directos, solo entrega las páginas para que el frontend cliente pida datos a la API.

## Carpeta `backend/usuarios`

### `models.py`
- Define `Usuario` como un `AbstractUser` extendido.
- Campos importantes:
  - `correo` como identificador único.
  - `tipo_usuario` con valores `estudiante` o `funcionario`.
- Cambia `USERNAME_FIELD` a `correo` para login por correo.
- `UsuarioManager` asegura creación correcta de usuarios y superusuarios.
- `get_by_natural_key` permite buscar al usuario por correo.

### `admin.py`
- Registra el modelo `Usuario` en el admin de Django.
- Muestra campos clave como correo, nombre y tipo de usuario.
- Permite buscar por correo, username, first_name y last_name.

### `views.py`
- `api_login`
  - Recibe `POST` con `correo` y `password`.
  - Usa `authenticate` y `login` de Django.
  - Devuelve perfil del usuario en JSON.
  - `@csrf_exempt` para compatibilidad con llamadas fetch desde el frontend.
- `api_register`
  - Recibe `POST` con nombre, correo, password y tipo.
  - Valida datos mínimos y dominio del correo.
  - Crea usuario con `create_user`.
  - Hace login automático y devuelve perfil.

### `management/commands/import_json_data.py`
- Comando Django para migrar datos del backend antiguo a Django.
- Usa `Path` y `json` para leer archivos.
- Si recibe argumento `archivo_json`, lee ese JSON consolidado.
- Si no recibe argumento, lee los archivos antiguos en `backend/data/`.
- Importa en este orden:
  1. usuarios
  2. salas
  3. reservas
  4. historial
  5. admin por defecto
- Funciones internas:
  - `importar_usuarios`
    - Acepta ruta a JSON o dict ya cargado.
    - Crea o actualiza usuarios por correo.
    - Usa `set_password` para almacenar el password seguro.
  - `importar_salas`
    - Crea o actualiza salas por `codigo`.
    - Traduce campos del JSON antiguo a los campos del modelo Django.
    - Marca `multimedia` como verdadero si no dice "no tiene".
  - `importar_reservas`
    - Busca usuario por `first_name` y sala por nombre.
    - Convierte fechas y rangos de hora.
    - Evita duplicados usando `external_id` o combinación de campo.
    - Llama a `marcar_bloque` para actualizar disponibilidad.
  - `importar_historial`
    - Crea registros de historial ligados a reservas existentes.
    - Si no encuentra reserva, guarda el historial con detalle.
  - `marcar_bloque`
    - Importa `marcar_bloque_por_fecha` desde `salas.views`.
    - Actualiza la disponibilidad de la sala cuando existe una reserva.
  - `crear_admin_por_defecto`
    - Crea o actualiza el admin `admin@admin.com` con contraseña `admin`.
  - `parse_date`, `parse_time`, `parse_range`
    - Convierte nombres de día y fechas del JSON antiguo a valores de fecha y hora.

## Carpeta `backend/salas`

### `models.py`
- Define `Sala` con campos:
  - `codigo`, `nombre`, `piso`, `capacidad`, `sillas`, `pizarra`, `multimedia`, `entorno`, `disponibilidad`, `activa`.
- `disponibilidad` guarda bloques semanales en formato JSON.
- Ordena por `codigo`.

### `views.py`
- Define utilidades de horario y disponibilidad.
- `normalizar_dia`, `date_for_day`, `day_key_from_date`
  - Convierten texto de día a clave y fecha real.
- `actualizar_disponibilidad`
  - Marca un bloque de horario como reservado o libre.
- `marcar_bloque_por_fecha`
  - Traduce fecha a día y llama a `actualizar_disponibilidad`.
- `sala_a_dict`
  - Convierte una sala a JSON usable por el frontend.
  - Revisa reservas activas y bloques de disponibilidad.
- `salas_api`
  - GET devuelve lista de salas activas para el mapa.
- `sala_detalle_api`
  - GET devuelve detalle de una sala.
  - PUT reserva un bloque específico de una sala.
  - `@csrf_exempt` para aceptar fetch directos del frontend.
- `sala_reservar_api`
  - Alias a `sala_detalle_api`.

## Carpeta `backend/reservas`

### `models.py`
- `Reserva`
  - Guarda reservas detectando sala, usuario, fecha y horas.
  - `external_id` mantiene vinculación con datos antiguos.
  - Restringe duplicados por sala/fecha/hora.
  - `estado` puede ser activa, cancelada o finalizada.
- `HistorialReserva`
  - Registra acciones sobre reservas.
  - Guarda detalle y referencia a la reserva.

### `views.py`
- `perfil_por_nombre`
  - Busca usuario por `first_name`.
  - Se usa porque los datos antiguos guardaban nombre del usuario en ese campo.
- `tabla_reservas_html` y `tabla_historial_html`
  - Generan HTML simple para mostrar en el frontend.
  - Devuelven filas `<tr>` con información de cada reserva o historial.
- `reservas_html`
  - GET devuelve reservas activas de un usuario.
  - DELETE borra una reserva por `external_id`.
  - Al borrar, actualiza disponibilidad y agrega historial.
- `reservas_all_html`
  - GET devuelve todas las reservas del sistema en HTML.
- `historial_html`
  - GET devuelve historial de un usuario.
- `crear_reserva`
  - POST crea una reserva nueva.
  - Valida usuario, sala, fecha y rango de hora.
  - Evita reservas duplicadas.
  - Marca el bloque como reservado en la sala.
  - Crea un registro de historial.
- `eliminar_reserva`
  - Alias de `reservas_html`.

## Carpeta `frontend`

### `templates/`
- Contiene todas las páginas HTML que Django sirve directamente.
- Páginas principales:
  - `index.html`
  - `login.html`
  - `mapa.html`
  - `detalleSalas.html`
  - `usuario.html`
  - `auth.html`
- Estas páginas contienen la interfaz y hacen peticiones a las rutas de API.

### `static/`
- Archivos de CSS y JS que usa el frontend.
- Se sirven desde Django gracias a `STATICFILES_DIRS`.
- Normalmente aquí van los estilos y scripts que actualizan la vista y consumen los endpoints.

## Carpeta `backend/data`

- Contiene los archivos JSON originales del proyecto anterior.
- Archivos:
  - `perfiles.json`: usuarios de estudiantes y funcionarios.
  - `salas.json`: datos de cada sala.
  - `reservas.json`: reservas heredadas.
  - `historial.json`: historial de acciones.
- Estos archivos son la fuente para el comando `import_json_data`.

## Flujo general de datos

1. El usuario visita una página en el navegador.
2. Django sirve el HTML desde `frontend/templates`.
3. El frontend hace fetch a las APIs en `config.urls`.
4. Las APIs usan vistas de `usuarios`, `salas` o `reservas`.
5. Las vistas consultan o escriben datos en la DB SQLite.
6. Si se importa información antigua, `import_json_data` lee JSON y crea registros Django.

## Por qué se importan estas librerías

- `Path` y `json` en `import_json_data`: para leer archivos y parsear JSON.
- `datetime` en importación y reservas: para convertir fechas y horas.
- `django.core.management.base.BaseCommand`: para crear el comando personalizado.
- `django.http.JsonResponse`: para devolver JSON al frontend.
- `csrf_exempt`: porque el frontend hace peticiones AJAX y no siempre manda token CSRF.
- `authenticate`, `login`: para manejar login con Django.
- `UserManager`, `AbstractUser`: para personalizar el usuario con correo.
- `settings.AUTH_USER_MODEL`: para referenciar el usuario personalizado desde otros modelos.

## Resumen rápido de archivos clave

- `manage.py`: arranca Django y ajusta import paths.
- `backend/config/settings.py`: configuración de rutas, DB, templates y static.
- `backend/config/urls.py`: define rutas públicas y API.
- `backend/config/views.py`: sirve HTML básico.
- `backend/usuarios/models.py`: modelo de usuario con correo.
- `backend/usuarios/views.py`: login y registro.
- `backend/usuarios/management/commands/import_json_data.py`: importación masiva.
- `backend/salas/models.py`: definición de sala.
- `backend/salas/views.py`: API de salas y disponibilidad.
- `backend/reservas/models.py`: reservas e historial.
- `backend/reservas/views.py`: creación, listado, eliminación e historial.
- `frontend/templates/`: código HTML visible por el navegador.
- `frontend/static/`: estilos y scripts que usa el frontend.
- `backend/data/`: datos legacy de entrada.

## Qué hace cada cosa y para qué sirve

- `backend/data/*.json` → fuente original de datos.
- `import_json_data` → convierte esos datos a Django.
- `usuarios` → define y gestiona logins/registraciones.
- `salas` → gestiona las salas y sus horarios.
- `reservas` → gestiona reservas, cancelaciones e historial.
- `frontend` → muestra el sistema al usuario.
- `config` → pega todo y hace que Django sirva páginas y APIs.
- `datos_iniciales.json` → alternativa de carga única para usar en lugar de varios archivos.
