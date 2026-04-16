let seleccion = null;

function cargarPagina() {
    const params = new URLSearchParams(window.location.search);
    const id = params.get('id') || "1"; // Por defecto la 1
    const sala = salasData[id];

    if (!sala) return;

    // Inyectar Datos en la Plantilla
    document.getElementById('sala-titulo').textContent = `Sala de Estudio ${sala.numero}`;
    document.getElementById('sala-piso').textContent = `Ubicación: ${sala.piso}`;
    document.getElementById('sala-img').src = sala.imagen;
    
    // Características Específicas
    document.getElementById('info-capacidad').textContent = `${sala.capacidad} Personas`;
    document.getElementById('info-sillas').textContent = `${sala.sillas} Sillas`;
    document.getElementById('info-pizarra').textContent = sala.pizarra;
    document.getElementById('info-tv').textContent = sala.television;
    document.getElementById('info-vista').textContent = `Vista al ${sala.vista}`;

    // Generar Tabla de Horarios
    const tbody = document.getElementById('tabla-body');
    tbody.innerHTML = '';

    sala.disponibilidad.forEach(item => {
        const tr = document.createElement('tr');
        let celdas = `<th scope="row" class="p-3 bg-slate-200 rounded-lg text-xs">${item.bloque}</th>`;
        
        ['lunes', 'martes', 'miercoles', 'jueves', 'viernes'].forEach(dia => {
            const libre = item[dia];
            const clase = libre ? 'slot-disponible' : 'slot-ocupado';
            const texto = libre ? 'Libre' : 'Ocupado';
            const estado = libre ? '' : 'disabled';
            
            celdas += `
                <td class="${clase}">
                    <button class="slot-btn" ${estado} onclick="marcar(this, '${item.bloque}', '${dia}')">
                        ${texto}
                    </button>
                </td>`;
        });
        tr.innerHTML = celdas;
        tbody.appendChild(tr);
    });
}

function marcar(btn, hora, dia) {
    document.querySelectorAll('.slot-btn').forEach(b => b.classList.remove('ring-4', 'ring-blue-600'));
    btn.classList.add('ring-4', 'ring-blue-600');
    seleccion = { hora, dia };
}

window.onload = cargarPagina;