# Taller 1 - CursoDesarrollo Soluc. Web/Móvil (12694-C1)

Este taller consiste en crear una pagina con login que diferencia entre alumnos y funcionarios. Luego de iniciar sesion, el usuario entra a una pagina con un mapa donde aparecen las salas. Al apretar una sala, se muestra un calendario con su disponibilidad, indicando que tan ocupada esta y en que horarios puedes reservarla.

El proyecto esta separado en `frontend/` y `backend/`.

## Prerrequisito (solo si no tienes Node.js)

Para usar `npm`, necesitas tener instalado Node.js.

Mini tutorial en Windows:

1. Descarga e instala la version LTS desde: https://nodejs.org
2. Durante la instalacion, deja marcada la opcion para agregar Node al PATH.
3. Cierra y vuelve a abrir la terminal.
4. Abre `CMD` (no PowerShell) y verifica:

```bat
node -v
npm -v
```

Si ambos comandos muestran version, ya puedes seguir con la ejecucion del proyecto.

## Instalacion de dependencias

El archivo `iniciar.bat` usa `npm run dev`, y ese comando depende de las dependencias del proyecto.

Antes de usarlo por primera vez, entra a la raiz del proyecto y ejecuta:

```bat
cd c:\ruta a tu carpeta\salas_biblioteca-main
npm install
```

Eso instala `express` y `nodemon` segun lo que esta definido en `package.json`.

No es necesario instalar `nodemon` de forma global. Si prefieres hacerlo globalmente, puedes usar:

```bat
npm install -g nodemon
```

pero para este proyecto no hace falta si ya ejecutaste `npm install`.

Si abres `iniciar.bat` y detecta que faltan dependencias, te preguntara antes de instalarlas. Si respondes que no, el script se detiene y debes ejecutar `npm install` manualmente.

## Como ejecutar

Opcion rapida en Windows:

- Haz doble clic en `iniciar.bat` desde la raiz del proyecto.
- Si es la primera vez, asegúrate de haber ejecutado antes `npm install` en la raiz.
- Se abre el backend y luego el navegador en `frontend/index.html`.

Opcion rapida en Linux/macOS:

```bash
chmod +x iniciar.sh
./iniciar.sh
```

Esto inicia el backend y abre `http://localhost:3000/index.html` en el navegador.

En carpeta `backend`:

```bash
cd c:\\ruta a tu carpeta\salas_biblioteca-main\backend
npm install
node server.js
```

Opcional (desde la raiz del proyecto) para desarrollo con reinicio automatico:

```bash
cd c:\\ruta a tu carpeta\salas_biblioteca-main
npm run dev
```

Ese comando requiere que `nodemon` ya este instalado en las dependencias del proyecto, por eso es importante correr `npm install` primero.

En carpeta `frontend`:

```bash
cd c:\\ruta a tu carpeta\salas_biblioteca-main\frontend
npx serve .
```

Si abres el proyecto desde el navegador, la entrada inicial tambien puede ser `frontend/index.html`, que redirige al login.

## Problemas comunes

Si `iniciar.bat` no abre bien el proyecto, revisa esto:

- Si aparece `npm no se reconoce como un comando`, instala Node.js otra vez y asegúrate de marcar la opcion para agregarlo al PATH.
- Si `npm run dev` falla porque falta `nodemon` o `express`, vuelve a ejecutar `npm install` en la raiz del proyecto.
- Si el navegador abre antes de que el backend termine de iniciar, espera unos segundos y recarga `http://localhost:3000/index.html`.
- Si el puerto `3000` ya esta en uso, cierra el proceso que lo esta ocupando o cambia la variable `PORT` antes de iniciar el backend.

## Nota

El archivo principal del backend en esta version es `backend/server.js`. Si prefieres usar `npm start` desde la raiz, tambien funciona porque el proyecto ya apunta a ese archivo.

## Estructura

- `frontend/`: paginas HTML, CSS e imagenes.
- `backend/`: API y datos persistidos en JSON.
- `backend/data/perfiles.json`: base de usuarios del sistema.

## Funciones del proyecto (documentacion simple)

### Backend (`backend/server.js`)

- `leerPerfiles()`:
	Lee `backend/data/perfiles.json` y retorna el objeto con reglas y usuarios.
	Ejemplo: si el JSON tiene estudiantes y funcionarios, devuelve todo ese contenido como objeto.

- `guardarPerfiles(data)`:
	Guarda en `backend/data/perfiles.json` el objeto completo recibido.
	Ejemplo: despues de crear un usuario nuevo, se llama con el objeto actualizado.

- `detectarTipo(correo, reglas)`:
	Determina si un correo es de `estudiante` o `funcionario` segun su dominio.
	Ejemplo: `ana@alumnos.ucn.cl` devuelve `estudiante`.
	Ejemplo: `pedro@funcionario.ucn.cl` devuelve `funcionario`.

- `obtenerListaPorTipo(data, tipo)`:
	Retorna `data.estudiantes` o `data.funcionarios` segun el tipo.
	Ejemplo: si el tipo es `estudiante`, devuelve la lista de estudiantes.

- `obtenerSiguienteId(lista, prefijo)`:
	Genera el siguiente ID disponible (por ejemplo `E005` o `F003`).
	Ejemplo: si el ultimo estudiante es `E004`, devuelve `E005`.

- `GET /`:
	Redirige al login (`/login.html`).
	Ejemplo: al abrir la raiz del proyecto en el navegador, manda al login.

- `POST /api/login`:
	Valida correo y password, busca usuario y devuelve perfil sin password.
	Ejemplo de entrada: `{ "correo": "ana@alumnos.ucn.cl", "password": "1234" }`.
	Ejemplo de salida: `{ "perfil": { "id": "E001", "nombre": "Ana", "correo": "...", "tipo": "estudiante" } }`.

- `POST /api/register`:
	Valida datos, crea usuario nuevo segun dominio, guarda en JSON y responde perfil creado.
	Ejemplo de entrada: `{ "nombre": "Luis", "correo": "luis@funcionario.ucn.cl", "password": "abc" }`.
	Ejemplo de salida: un perfil nuevo guardado en el JSON y devuelto sin password.

- `app.listen(port, ...)`:
	Levanta el servidor en el puerto configurado.
	Ejemplo: si el puerto es 3000, el backend queda en `http://localhost:3000`.

### Frontend (`frontend/login.html`)

- `mostrarMensaje(elemento, texto, esError)`:
	Muestra mensajes de error/exito con estilos en los formularios.
	Ejemplo: muestra en rojo un error de login o en verde un acceso correcto.

- `submit` de `loginForm`:
	Llama a `/api/login`, guarda `perfilActivo` en `localStorage` y redirige a `Piso1.html`.
	Ejemplo: si el login es correcto, el usuario va a Piso1 sin recargar manualmente.

- `submit` de `registerForm`:
	Llama a `/api/register`, muestra resultado y limpia el formulario.
	Ejemplo: si el usuario se crea bien, el formulario se vacia y aparece un mensaje de exito.

### Frontend (`frontend/Piso1.html`)

- Funcion autoejecutable `(function () { ... })()`:
	Inicializa la vista, lee `perfilActivo` y muestra si el usuario es alumno o funcionario.
	Ejemplo: si el perfil guardado dice `estudiante`, en pantalla aparece `Eres alumno.`.

- `click` de `#cerrarSesion`:
	Elimina `perfilActivo` de `localStorage` y vuelve a `login.html`.
	Ejemplo: al tocar el boton, la sesion local se borra y el usuario vuelve al login.

### Frontend sin funciones JS por ahora

- `frontend/characteristics.html`: vista estatica de sala y disponibilidad.
- `frontend/pisoNeg1.html`: pagina basica de navegacion.

## Resumen rapido para reutilizar

- Si necesitas leer usuarios: usa `leerPerfiles()`.
- Si necesitas guardar cambios en usuarios: usa `guardarPerfiles(data)`.
- Si necesitas saber si un correo es alumno o funcionario: usa `detectarTipo(correo, reglas)`.
- Si necesitas crear un nuevo ID: usa `obtenerSiguienteId(lista, prefijo)`.
- Si necesitas iniciar sesion: usa `POST /api/login`.
- Si necesitas crear usuarios: usa `POST /api/register`.
