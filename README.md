# Salas Biblioteca UCN

Sistema de reserva de salas con Django REST Framework en el backend y HTML/JS vanilla en el frontend.

## Estructura

```
salas_biblioteca/
├── manage.py
├── requirements.txt
├── .env.example          ← copia esto como .env
├── config/               ← configuración de Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── usuario/              ← app: registro, login, usuarios
├── salas/                ← app: salas y disponibilidades
├── reservas/             ← app: reservas, historial y comando cargar_datos
│   └── management/commands/cargar_datos.py
├── frontend/             ← HTML, CSS y JS servidos por Django
│   ├── index.html
│   ├── login.html
│   ├── mapa.html
│   ├── usuario.html
│   ├── detalleSalas.html
│   ├── css/
│   ├── js/
│   └── img/
└── data/                 ← JSONs con datos iniciales
```

## Instalación

```bash
# 1. Crear entorno virtual e instalar dependencias
python -m venv venv
source venv/bin/activate   # Linux
venv\Scripts\activate      # Windows 
pip install -r requirements.txt

# 2. Configurar variables de entorno
cp .env.example .env
# edita .env y cambia SECRET_KEY

python manage.py makemigrations usuario
python manage.py makemigrations salas
python manage.py makemigrations reservas

# 3. Crear la base de datos
python manage.py migrate

# 4. Cargar datos de ejemplo desde los JSON
python manage.py cargar_datos

# 5. (Opcional) Crear superusuario para el admin
python manage.py createsuperuser

# 6. Levantar el servidor
python manage.py runserver
```

Abre http://localhost:8000 en el navegador.

## Endpoints de la API

| Método | URL | Descripción |
|--------|-----|-------------|
| POST | `/api/usuarios/login/` | Iniciar sesión |
| POST | `/api/usuarios/register/` | Registrar usuario |
| GET | `/api/usuarios/` | Listar usuarios |
| GET | `/api/salas/` | Listar salas |
| GET | `/api/salas/<numero>/` | Detalle de sala con disponibilidades |
| GET | `/api/salas/disponibilidades/?sala=<numero>` | Disponibilidades de una sala |
| GET | `/api/reservas/?usuario=<id>` | Reservas de un usuario |
| POST | `/api/reservas/` | Crear reserva |
| DELETE | `/api/reservas/<id>/` | Cancelar reserva |
| GET | `/api/reservas/historial/?usuario=<id>` | Historial de un usuario |

## Páginas

| URL | Archivo |
|-----|---------|
| `/` | `frontend/index.html` |
| `/login/` | `frontend/login.html` |
| `/mapa/` | `frontend/mapa.html` |
| `/usuario/` | `frontend/usuario.html` |
| `/detalle-sala/?id=<numero>` | `frontend/detalleSalas.html` |
