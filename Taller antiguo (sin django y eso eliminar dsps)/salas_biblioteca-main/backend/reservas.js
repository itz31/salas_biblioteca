const fs = require("fs")
const path = require("path")


const leerReservas = () => {
  const dataPath = path.join(__dirname, "data", "reservas.json")
  const contenido = fs.readFileSync(dataPath, "utf-8")
  const parse = JSON.parse(contenido)
  return parse
}

const guardarReservas = (data) => {
  const dataPath = path.join(__dirname, "data", "reservas.json")
  // JSON.stringify(data, null, 2) formatea el JSON para que sea legible (con indentación)
  fs.writeFileSync(dataPath, JSON.stringify(data, null, 2), "utf-8")
}

const crearReserva = (nuevaReserva) => {
  const contenido = leerReservas()
  contenido.push(nuevaReserva) // Modificamos el arreglo en memoria
  guardarReservas(contenido)   // Sobrescribimos el archivo JSON
}

const eliminarReserva = (idReserva) => {
  const contenido = leerReservas()
  // Filtramos las reservas, dejando todas excepto la que queremos eliminar
  const nuevoContenido = contenido.filter(reserva => reserva.id !== idReserva)
  guardarReservas(nuevoContenido) // Sobrescribimos el archivo JSON con la lista filtrada
}

const crearTablaReservas = reservas => {
  return reservas.map(reserva => `
    <tr class="border-b border-slate-100 hover:bg-slate-50 transition" data-id="${reserva.id}">
      <td class="p-3 text-slate-700">${reserva.sala}</td>
      <td class="p-3 text-slate-600">${reserva.fecha}</td>
      <td class="p-3 text-slate-600">${reserva.hora}</td>
    </tr>
  `).join('');
}

const listReservas = nombreUsuario => {
  const contenido = leerReservas();
  const filtradas = contenido.filter(reserva => reserva.nombreUsuario === nombreUsuario);

  if (filtradas.length === 0) {
    return '<tr><td colspan="4" class="text-center p-4">No tienes reservas activas.</td></tr>';
  }

  return crearTablaReservas(filtradas)
}

const listAllReservas = () => {
  const contenido = leerReservas()
  if (contenido.length === 0) {
    return '<tr><td colspan="4" class="text-center p-4">no hay ninguna reserva</td></tr>';
  }
  return crearTablaReservas(contenido)
}

module.exports = { leerReservas, crearReserva, eliminarReserva, listReservas, listAllReservas}