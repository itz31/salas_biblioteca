# Sistema de Reservas de Salas de Biblioteca

Proyecto migrado a **Django** para el taller. La base actual ya incluye:

- Proyecto Django funcional.
- Modelos principales para usuarios, salas, reservas e historial.
- Panel de administración de Django.
- Base de datos SQLite.
- Comando para importar los datos antiguos desde los JSON del backend anterior.

## Estructura actual

- `config/`: configuración principal del proyecto Django.
- `usuarios/`: modelo de usuario personalizado y comandos de importación.
- `salas/`: modelo de salas.
- `reservas/`: modelo de reservas e historial.
- `templates/`: vistas HTML de Django.
- `backend/data/`: datos antiguos en JSON que pueden importarse a Django.
- `frontend/`: archivos estáticos y vistas visuales del prototipo anterior.

## Requisitos

- Python instalado en Windows.
- El entorno virtual `.venv` dentro de la raíz del proyecto.
- Dependencias instaladas con `pip`.

## Cómo iniciar el proyecto

### Opción recomendada

Haz doble clic en `iniciar.bat` desde la raíz del proyecto.

Ese archivo hace lo siguiente:

1. Verifica que exista el entorno virtual.
2. Instala las dependencias de `requirements.txt` si hace falta.
3. Aplica las migraciones de Django.
4. Importa los datos iniciales desde `backend/data/*.json`.
5. Levanta el servidor con `runserver`.
6. Abre el navegador en `http://127.0.0.1:8000`.

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

### 1. Pantalla principal

Al abrir el proyecto verás una página simple de inicio generada por Django. Esa página confirma que el proyecto ya está corriendo correctamente.

### 2. Panel de administración

Entra a:

```text
http://127.0.0.1:8000/admin/
```

Ahí puedes revisar y administrar:

- Usuarios.
- Salas.
- Reservas.
- Historial de reservas.

### 3. Datos iniciales importados

El comando `import_json_data` toma la información que ya existía en:

- `backend/data/perfiles.json`
- `backend/data/salas.json`
- `backend/data/reservas.json`
- `backend/data/historial.json`

Y la pasa al nuevo modelo de Django.

## Comando útil

Si quieres recargar los datos antiguos manualmente:

```bat
python manage.py import_json_data
```

## Modelo de trabajo recomendado para el taller

La base ya quedó lista para que el equipo siga así:

1. Autenticación y roles.
2. Listado de salas y detalle.
3. Reservas e historial.
4. Ajustes de frontend o templates.

## Archivos clave

- [config/settings.py](config/settings.py): configuración del proyecto.
- [usuarios/models.py](usuarios/models.py): usuario personalizado.
- [salas/models.py](salas/models.py): modelo de salas.
- [reservas/models.py](reservas/models.py): reservas e historial.
- [usuarios/management/commands/import_json_data.py](usuarios/management/commands/import_json_data.py): importación desde JSON.
- [iniciar.bat](iniciar.bat): arranque rápido en Windows.

## Nota

El archivo `iniciar.sh` fue eliminado porque ya no corresponde al flujo real del proyecto y no funcionaba para la base actual en Django.
