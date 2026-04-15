# Taller 1 - CursoDesarrollo Soluc. Web/Móvil (12694-C1)

Este taller consiste en crear una pagina con login que diferencia entre alumnos y funcionarios. Luego de iniciar sesion, el usuario entra a una pagina con un mapa donde aparecen las salas. Al apretar una sala, se muestra un calendario con su disponibilidad, indicando que tan ocupada esta y en que horarios puedes reservarla.

El proyecto esta separado en `frontend/` y `backend/`.

## Como ejecutar

En carpeta `backend`:

```bash
cd c:\\ruta a tu carpeta\salas_biblioteca-main\backend
npm install
node server.js
```

En carpeta `frontend`:

```bash
cd c:\\ruta a tu carpeta\salas_biblioteca-main\frontend
npx serve .
```

## Nota

El archivo principal del backend en esta version es `backend/server.js`. Si prefieres usar `npm start` desde la raiz, tambien funciona porque el proyecto ya apunta a ese archivo.

## Estructura

- `frontend/`: paginas HTML, CSS e imagenes.
- `backend/`: API y datos persistidos en JSON.
- `backend/data/perfiles.json`: base de usuarios del sistema.
