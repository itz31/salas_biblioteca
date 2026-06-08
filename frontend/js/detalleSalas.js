(async function () {
    const urlParams = new URLSearchParams(window.location.search);
    const idSala = urlParams.get('id');

    if (!idSala) {
        const titulo = document.getElementById('sala-titulo');
        if (titulo) titulo.textContent = 'Error: Sala no especificada';
        return;
    }

    const cargarPerfil = () => JSON.parse(localStorage.getItem('perfilActivo'));

    async function cargarDetalles() {
        try {
            const respuesta = await fetch(`/api/salas/${idSala}/`);
            if (!respuesta.ok) throw new Error('Sala no encontrada');
            const sala = await respuesta.json();

            document.getElementById('sala-titulo').textContent = `Sala ${sala.numero}`;
            document.getElementById('sala-piso').textContent = `Piso ${sala.piso}`;
            document.getElementById('info-capacidad').textContent = `${sala.capacidad} personas`;
            document.getElementById('info-sillas').textContent = sala.sillas;
            document.getElementById('info-pizarra').textContent = sala.pizarra;
            document.getElementById('info-tv').textContent = sala.television;
            document.getElementById('info-vista').textContent = sala.vista;

            renderizarTabla(sala.disponibilidades || []);
        } catch (error) {
            console.error('Error al cargar los detalles:', error);
            document.getElementById('sala-titulo').textContent = 'Error al conectar con el servidor';
        }
    }

    function renderizarTabla(disponibilidades) {
        const tbody = document.getElementById('tabla-body');
        tbody.innerHTML = '';

        if (!disponibilidades.length) {
            tbody.innerHTML = '<tr><td colspan="4" class="p-4 text-slate-500">No hay horarios registrados.</td></tr>';
            return;
        }

        disponibilidades.forEach(disp => {
            const tr = document.createElement('tr');
            tr.className = 'border-b border-slate-100 hover:bg-slate-50 transition';

            const [horaInicio, horaFin] = disp.bloque.split(' - ');

            tr.innerHTML = `
                <td class="p-3">${disp.dia}</td>
                <td class="p-3">${horaInicio || disp.bloque}</td>
                <td class="p-3">${horaFin || ''}</td>
                <td class="p-3 font-bold ${disp.disponible ? 'text-green-600' : 'text-red-600'}">
                    ${disp.disponible ? 'Disponible' : 'Reservada'}
                </td>
                <td class="p-3" id="btn-${disp.id}"></td>
            `;
            tbody.appendChild(tr);

            const tdAccion = document.getElementById(`btn-${disp.id}`);
            if (!disp.disponible) {
                const span = document.createElement('span');
                span.className = 'text-slate-400 text-xs italic';
                span.textContent = 'No disponible';
                tdAccion.appendChild(span);
            } else {
                const btn = document.createElement('button');
                btn.textContent = 'Reservar';
                btn.className = 'bg-blue-600 hover:bg-blue-700 text-white px-4 py-1 rounded text-sm font-semibold transition shadow-sm';
                btn.onclick = () => hacerReserva(disp);
                tdAccion.appendChild(btn);
            }
        });
    }

    async function hacerReserva(disp) {
        const perfil = cargarPerfil();
        if (!perfil) {
            alert('Debes iniciar sesión para reservar.');
            window.location.href = '/login/';
            return;
        }

        const [horaInicio, horaFin] = disp.bloque.split(' - ');
        if (!confirm(`¿Confirmas la reserva para el ${disp.dia} de ${horaInicio} a ${horaFin}?`)) return;

        try {
            const respuesta = await fetch('/api/reservas/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    usuario: perfil.id_usuario,
                    sala: idSala,
                    disponibilidad: disp.id,
                    fecha: new Date().toISOString().split('T')[0],
                    hora: disp.bloque,
                }),
            });

            if (!respuesta.ok) {
                const err = await respuesta.json();
                throw new Error(JSON.stringify(err));
            }

            alert('¡Reserva realizada con éxito!');
            cargarDetalles();
        } catch (error) {
            console.error('Error al reservar:', error);
            alert('Hubo un problema al procesar tu reserva.');
        }
    }

    cargarDetalles();
})();
