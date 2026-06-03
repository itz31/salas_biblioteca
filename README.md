# Sistema de Reservas de Salas de Biblioteca

Proyecto reorganizado para funcionar solo con **Django** y **SQLite**.

## Qué incluye ahora

- Proyecto Django funcional.
- Base de datos SQLite en `db.sqlite3`.
- Usuario personalizado con login por correo.
- Modelos para salas, reservas e historial.
- Panel de administración de Django.
- Comando para importar los datos antiguos desde los JSON del backend anterior.
- Inicio rápido en Windows con `iniciar.bat`.

## Estructura actual

- `config/`: configuración principal del proyecto Django.
- `usuarios/`: modelo de usuario personalizado y comando de importación.
- `salas/`: modelo de salas.
- `reservas/`: modelo de reservas e historial.
- `templates/`: vistas HTML de Django.
- `backend/data/`: JSON antiguos que sirven como datos iniciales.

## Cómo iniciar el proyecto

### Opción recomendada

Haz doble clic en `iniciar.bat` desde la raíz del proyecto.

Ese archivo hace esto:

1. Verifica que exista el entorno virtual.
2. Instala las dependencias de `requirements.txt` si hace falta.
3. Aplica las migraciones de Django.
4. Importa los datos iniciales desde `backend/data/*.json`.
5. Crea la cuenta admin `admin@admin.com` con contraseña `admin`.
6. Levanta el servidor con `runserver`.
7. Abre el navegador en `http://127.0.0.1:8000`.

### Opción manual

Desde la raíz del proyecto:

```bat
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py import_json_data
python manage.py runserver
```

Después abre:

```text
http://127.0.0.1:8000
```

## Cómo usar lo que ya está hecho

### Pantalla principal

Al abrir el proyecto verás una página simple de inicio generada por Django. Esa página confirma que el proyecto ya está corriendo correctamente.

### Panel de administración

Entra a:

```text
http://127.0.0.1:8000/admin/
```

Credenciales del admin:

- Correo: `admin@admin.com`
- Contraseña: `admin`

Ahí puedes revisar y administrar:

- Usuarios.
- Salas.
- Reservas.
- Historial de reservas.

### Datos iniciales importados

El comando `import_json_data` toma la información que existe en:

- `backend/data/perfiles.json`
- `backend/data/salas.json`
- `backend/data/reservas.json`
- `backend/data/historial.json`

y la pasa al modelo de Django.

## Comando útil

Si quieres recargar los datos antiguos manualmente:

```bat
python manage.py import_json_data
```

## Modelo de trabajo recomendado

La base ya quedó lista para que el equipo siga así:

1. Autenticación y roles.
2. Listado de salas y detalle.
3. Reservas e historial.
4. Ajustes de templates o vistas de Django.

## Archivos clave

- [config/settings.py](config/settings.py): configuración del proyecto.
- [usuarios/models.py](usuarios/models.py): usuario personalizado.
- [salas/models.py](salas/models.py): modelo de salas.
- [reservas/models.py](reservas/models.py): reservas e historial.
- [usuarios/management/commands/import_json_data.py](usuarios/management/commands/import_json_data.py): importación desde JSON.
- [iniciar.bat](iniciar.bat): arranque rápido en Windows.

## Nota

El archivo `iniciar.sh` fue eliminado porque ya no corresponde al flujo real del proyecto. El frontend viejo y el backend Node/Express también fueron retirados para dejar solo la versión Django.
