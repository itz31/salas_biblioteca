(async function() {
  const urlParams = new URLSearchParams(window.location.search);
  const idSala = urlParams.get('id');
  let nombreSalaGlobal = "";

  if (!idSala) {
    const titulo = document.getElementById('sala-titulo');
    if (titulo) titulo.textContent = "Error: Sala no especificada";
      return;
    }

  const cargarPerfil = () => JSON.parse(localStorage.getItem('perfilActivo'));

  async function cargarDetalles() {
        try {
            const respuesta = await fetch(`/salas/${idSala}`);
            const datos = await respuesta.json();

            if (datos && datos.length > 0) {
                const sala = datos[0];
                nombreSalaGlobal = sala.nombre;

                // Actualizar interfaz
                document.getElementById('sala-titulo').textContent = sala.nombre;
                document.getElementById('sala-piso').textContent = `Piso ${sala.piso}`;
                document.getElementById('info-capacidad').textContent = `${sala.capacidad} personas`;
                document.getElementById('info-sillas').textContent = sala.sillas;
                document.getElementById('info-pizarra').textContent = sala.pizarra;
                document.getElementById('info-tv').textContent = sala.multimedia ? "Sí" : "No";
                document.getElementById('info-vista').textContent = sala.entorno;

                renderizarTabla(sala.horarios);
            } else {
                document.getElementById('sala-titulo').textContent = "Sala no encontrada";
            }
        } catch (error) {
            console.error("Error al cargar los detalles:", error);
            document.getElementById('sala-titulo').textContent = "Error al conectar con el servidor";
        }
    }

    function renderizarTabla(horarios) {
        const tbody = document.getElementById('tabla-body');
        tbody.innerHTML = '';

        if (horarios && horarios.length > 0) {
            horarios.forEach(horario => {
                const tr = document.createElement('tr');
                tr.className = 'border-b border-slate-100 hover:bg-slate-50 transition';

                tr.innerHTML = `
                    <td class="p-3">${horario.dia}</td>
                    <td class="p-3">${horario.hora_inicio}</td>
                    <td class="p-3">${horario.hora_finalizacion}</td>
                    <td class="p-3 font-bold ${horario.reservada ? 'text-red-600' : 'text-green-600'}">
                        ${horario.reservada ? 'Reservada' : 'Disponible'}
                    </td>
                    <td class="p-3" id="btn-container-${horario.hora_inicio.replace(':', '')}"></td>
                `;

                tbody.appendChild(tr);

                // Agregar botón o texto de disponibilidad
                const tdAccion = tr.querySelector(`#btn-container-${horario.hora_inicio.replace(':', '')}`);
                if (horario.reservada) {
                    const spanOcupado = document.createElement('span');
                    spanOcupado.className = "text-slate-400 text-xs italic";
                    spanOcupado.textContent = "No disponible";
                    tdAccion.appendChild(spanOcupado);
                } else {
                    const btnReservar = document.createElement('button');
                    btnReservar.textContent = 'Reservar';
                    btnReservar.className = 'bg-blue-600 hover:bg-blue-700 text-white px-4 py-1 rounded text-sm font-semibold transition shadow-sm';
                    btnReservar.onclick = () => hacerReserva(horario);
                    tdAccion.appendChild(btnReservar);
                }
            });
        } else {
            tbody.innerHTML = '<tr><td colspan="5" class="p-4 text-slate-500">No hay horarios registrados.</td></tr>';
        }
    }

    async function hacerReserva(horario) {
        const perfil = cargarPerfil();
        if (!perfil) {
            alert("Debes iniciar sesión para reservar.");
            window.location.href = "login.html";
            return;
        }

        if (!confirm(`¿Confirmas la reserva para el ${horario.dia} de ${horario.hora_inicio} a ${horario.hora_finalizacion}?`)) {
            return;
        }

        try {
            // 1. Marcar como reservado en el servidor
            const putRespuesta = await fetch(`/salas/${idSala},${horario.hora_inicio}`, {
              method: 'PUT',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ dia: horario.dia })
});

            if (!putRespuesta.ok) throw new Error("Error al actualizar la disponibilidad de la sala");

            // 2. Crear el registro de la reserva
            const nuevaReserva = {
                id: "res-" + Date.now(),
                nombreUsuario: perfil.nombre,
                sala: nombreSalaGlobal,
                fecha: horario.dia,
                hora: `${horario.hora_inicio} - ${horario.hora_finalizacion}`
            };

            const postRespuesta = await fetch("/reservas", {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(nuevaReserva)
            });

            if (!postRespuesta.ok) throw new Error("Error al registrar la reserva en tu perfil");

            alert("¡Reserva realizada con éxito!");
            cargarDetalles(); 

        } catch (error) {
            console.error("Error al reservar:", error);
            alert("Hubo un problema al procesar tu reserva.");
        }
    }

    // Inicializar la carga de datos
    cargarDetalles();

})();