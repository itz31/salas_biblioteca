# Migración del Taller 1 al Taller actual

Este documento explica paso a paso cómo se transformó el proyecto del taller anterior a la versión actual con Django y la estructura `frontend/backend`.

## 1. Estado inicial del Taller 1

En el taller anterior se tenía un proyecto con backend antiguo y frontend heredado. El código estaba mezclado y el frontend ya existía como páginas HTML independientes que consumían APIs de un backend no Django.

El objetivo fue:

- conservar la UI antigua del taller.
- reemplazar todo el backend antiguo por un backend Django.
- reorganizar el repositorio para que tenga solo `frontend/` y `backend/`.
- mantener la posibilidad de cargar datos antiguos desde JSON.

## 2. Preparar la estructura final

Se creó la estructura esperada:

- `backend/`: aquí va todo lo relacionado con Django.
- `frontend/`: aquí van las plantillas y archivos estáticos.
- `manage.py`: en la raíz para arrancar el proyecto desde el nivel superior.
- `datos_iniciales.json`: seed inicial consolidado.

## 3. Mover el frontend al nuevo layout

Acción:

- tomar las páginas HTML que ya estaban funcionando y moverlas a `frontend/templates/`.
- poner CSS y JS en `frontend/static/`.
- dejar el frontend igual visualmente, pero servido por Django.

Resultado:

- Django puede servir `login.html`, `mapa.html`, `detalleSalas.html`, `usuario.html`, etc.
- Las rutas de las páginas quedan claras y resuelven desde `config.views`.

## 4. Crear el backend Django dentro de `backend/`

Acción:

- inicializar un proyecto Django dentro de `backend/config`.
- crear apps Django para cada dominio:
  - `usuarios`
  - `salas`
  - `reservas`

Resultado:

- `backend/config/settings.py` controla DB, plantillas y estáticos.
- `backend/config/urls.py` mapea front y APIs.
- `backend/config/views.py` solo sirve los HTML.

## 5. Ajustar `manage.py` para la nueva ubicación

Problema:

- `manage.py` está en la raíz, pero el proyecto Django está en `backend/config`.

Solución:

- añadir `backend/` al `sys.path` en `manage.py`.
- dejar `DJANGO_SETTINGS_MODULE` apuntando a `config.settings`.

Esto permite ejecutar comandos como:

```bat
python manage.py migrate
python manage.py runserver
python manage.py import_json_data
```

## 6. Configurar settings para usar frontend heredado

Cambios en `backend/config/settings.py`:

- `ROOT_DIR` apunta a la carpeta raíz.
- `TEMPLATES['DIRS']` incluye `ROOT_DIR / 'frontend' / 'templates'`.
- `STATICFILES_DIRS` incluye `ROOT_DIR / 'frontend' / 'static'`.
- `DATABASES` usa `sqlite3` en `ROOT_DIR / 'db.sqlite3'`.
- `AUTH_USER_MODEL` se cambia a `usuarios.Usuario`.

## 7. Crear el modelo de usuario personalizado

Se creó `backend/usuarios/models.py` para:

- usar correo como campo de login.
- agregar tipo de usuario (`estudiante` / `funcionario`).
- mantener compatibilidad con Django auth.

También se creó `backend/usuarios/admin.py` para registrar el modelo en el admin.

## 8. Importar datos antiguos desde JSON

Se construyó un comando custom en `backend/usuarios/management/commands/import_json_data.py`.

Qué hace:

- lee `datos_iniciales.json` si se pasa como argumento.
- o lee los archivos antiguos en `backend/data/`.
- importa usuarios, salas, reservas e historial.
- crea un admin por defecto `admin@admin.com` / `admin`.

Esto permitió reutilizar la data heredada sin mantener el backend antiguo.
E igual aveces git corrompe el archivo de la base de datos como esta en binario asi que vi necesario
el tener el archivo json para poder guardar los datos en el github (que no es una buena idea en casos reales pq pos se te filtra todo)

## 9. Implementar APIs y lógica de reservas

Se creó lógica en dos apps:

- `backend/salas/`
  - modelo `Sala`.
  - APIs para listar salas y ver detalle.
  - funciones para marcar bloques de horario.
- `backend/reservas/`
  - modelo `Reserva`.
  - modelo `HistorialReserva`.
  - APIs para crear reservas, listar reservas e historial, eliminar reservas.

Rutas importantes en `backend/config/urls.py`:

- `/api/login`
- `/api/register`
- `/salas`
- `/salas/<param>`
- `/reservas`
- `/reservas/<param>`
- `/historial/<param>`

## 10. Conectar el frontend con el backend Django

Acción:

- las páginas HTML quedaron servidas desde Django.
- el frontend sigue haciendo peticiones a las rutas API.
- se añadieron `@csrf_exempt` en endpoints que reciben fetch desde JS.

Resultado:

- el frontend heredado pudo seguir funcionando sin reescribir la UI.
- el backend nuevo respondió a las mismas necesidades de datos.

## 11. Generar el seed consolidado

Se creó `datos_iniciales.json` en la raíz.

Qué contiene:

- `usuarios`
- `salas`
- `reservas`
- `historial`

Para facilitar la importación con un solo archivo en lugar de cuatro archivos separados.

## 12. Actualizar documentación

Se añadieron:

- `README.md` con la nueva estructura y comandos.
- `DOCUMENTACION.md` con descripción técnica del proyecto.
- `MIGRACION_TALLER_1_A_TALLER_2.md` este archivo que es para ordenarse solamente, super fan de los markdowns.

## 13. Resultado final

El proyecto quedó así:

- la vista del taller antiguo se mantiene,
- el backend antiguo se reemplazó por Django,
- el repositorio solo tiene `frontend/` y `backend/`,
- los datos antiguos se pueden importar con `import_json_data`.

### Comando de arranque recomendado

```bat
python manage.py migrate
python manage.py import_json_data datos_iniciales.json
python manage.py runserver
```

### Direcciones de interés

- `http://127.0.0.1:8000/login.html`
- `http://127.0.0.1:8000/mapa.html`
- `http://127.0.0.1:8000/detalleSalas.html`
- `http://127.0.0.1:8000/usuario.html`
- `http://127.0.0.1:8000/admin/`
