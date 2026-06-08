 (function () {
    const cargarPerfil = () => JSON.parse(localStorage.getItem('perfilActivo'));

    const perfil = cargarPerfil();
    if (!perfil) {
      window.location.href = '/login/';
      return;
    }

    document.getElementById('Usuario h1').textContent = perfil.nombre;
    document.getElementById('Usuario cargo').textContent = `Cargo: ${perfil.tipo}`;

    async function cargarReservas() {
      const tbody = document.getElementById('reservas-body');
      try {
        const res = await fetch(`/api/reservas/?usuario=${perfil.id_usuario}`);
        if (!res.ok) throw new Error();
        const data = await res.json();
        const reservas = data.results || data;

        if (!reservas.length) {
          tbody.innerHTML = '<tr><td colspan="4" class="p-4 text-center text-slate-500">No tienes reservas activas.</td></tr>';
          return;
        }

        tbody.innerHTML = reservas.map(r => `
          <tr data-id="${r.id}" class="border-b border-slate-100">
            <td class="p-3">Sala ${r.sala_numero}</td>
            <td class="p-3">${r.fecha}</td>
            <td class="p-3">${r.hora}</td>
            <td class="p-3">
              <button onclick="eliminarReserva(${r.id})" class="text-red-500 hover:text-red-700 font-medium transition">Eliminar</button>
            </td>
          </tr>
        `).join('');
      } catch {
        tbody.innerHTML = '<tr><td colspan="4" class="p-4 text-center text-red-500">Error al cargar la información.</td></tr>';
      }
    }

    async function cargarHistorial() {
      const tbody = document.getElementById('historial-body');
      try {
        const res = await fetch(`/api/reservas/historial/?usuario=${perfil.id_usuario}`);
        if (!res.ok) throw new Error();
        const data = await res.json();
        const historial = data.results || data;

        if (!historial.length) {
          tbody.innerHTML = '<tr><td colspan="3" class="p-4 text-center text-slate-500">No hay historial disponible.</td></tr>';
          return;
        }

        tbody.innerHTML = historial.map(h => `
          <tr class="border-b border-slate-100">
            <td class="p-3">Sala ${h.sala_numero}</td>
            <td class="p-3">${h.fecha}</td>
            <td class="p-3">${h.hora}</td>
          </tr>
        `).join('');
      } catch {
        tbody.innerHTML = '<tr><td colspan="3" class="p-4 text-center text-red-500">Error al cargar el historial.</td></tr>';
      }
    }

    window.eliminarReserva = async function (id) {
      if (!confirm('¿Estás seguro de que deseas eliminar esta reserva?')) return;
      try {
        const res = await fetch(`/api/reservas/${id}/`, { method: 'DELETE' });
        if (!res.ok) throw new Error();
        cargarReservas();
      } catch {
        alert('Hubo un problema al eliminar la reserva.');
      }
    };

    cargarReservas();
    cargarHistorial();
  })();