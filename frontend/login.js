const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');
const loginMessage = document.getElementById('loginMessage');
const registerMessage = document.getElementById('registerMessage');
const apiBase = '/api';

// Muestra mensajes de exito/error en pantalla reutilizando estilos existentes.
function mostrarMensaje(elemento, texto, esError) {
    elemento.textContent = texto;
    elemento.classList.remove('hidden', 'text-red-600', 'text-green-700');
    elemento.classList.add(esError ? 'text-red-600' : 'text-green-700');
}

// Maneja el envio del formulario de login y guarda el perfil activo en localStorage.
loginForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const correo = document.getElementById('loginEmail').value.trim().toLowerCase();
    const password = document.getElementById('loginPassword').value;

    try {
        const respuesta = await fetch(`${apiBase}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ correo, password })
        });

        const data = await respuesta.json();

        if (!respuesta.ok) {
            mostrarMensaje(loginMessage, data.mensaje || 'No fue posible iniciar sesión.', true);
            return;
        }

        localStorage.setItem('perfilActivo', JSON.stringify(data.perfil));
        mostrarMensaje(loginMessage, 'Acceso correcto. Redirigiendo...', false);
        window.location.href = 'mapa.html';
    } catch (error) {
        mostrarMensaje(loginMessage, 'No se pudo conectar con el servidor. Inicia el backend.', true);
    }
});

// Maneja el formulario de registro para crear usuarios nuevos en el backend.
registerForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const nombre = document.getElementById('nombre').value.trim();
    const correo = document.getElementById('registerEmail').value.trim().toLowerCase();
    const password = document.getElementById('registerPassword').value;

    try {
        const respuesta = await fetch(`${apiBase}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nombre, correo, password })
        });

        const data = await respuesta.json();

        if (!respuesta.ok) {
            mostrarMensaje(registerMessage, data.mensaje || 'No fue posible crear el usuario.', true);
            return;
        }

        mostrarMensaje(registerMessage, `Usuario creado como ${data.perfil.tipo}. Ya puedes iniciar sesión.`, false);
        registerForm.reset();
    } catch (error) {
        mostrarMensaje(registerMessage, 'No se pudo conectar con el servidor. Inicia el backend.', true);
    }
});
