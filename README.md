# Taller 1 - CursoDesarrollo Soluc. Web/Móvil (12694-C1)

Este taller consiste en crear una pagina con login que diferencia entre alumnos y funcionarios. Luego de iniciar sesion, el usuario entra a una pagina con un mapa donde aparecen las salas. Al apretar una sala, se muestra un calendario con su disponibilidad, indicando que tan ocupada esta y en que horarios puedes reservarla.

El proyecto esta separado en `frontend/` y `backend/`.

## Como ejecutar

En carpeta `backend`:

```bash
npm install
node app.js
```

En carpeta `frontend`:

```bash
npx serve .
```

## Nota

Si el archivo principal del backend no se llama `app.js`, reemplaza ese nombre por el archivo real del servidor. En esta version del proyecto el backend vive dentro de la carpeta `backend/` y expone la API para el login y el registro.

## Estructura

- `frontend/`: paginas HTML, CSS e imagenes.
- `backend/`: API y datos persistidos en JSON.
- `backend/data/perfiles.json`: base de usuarios del sistema.
