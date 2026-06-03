
const fs = require("fs")
const path =  require("path")

const leerJson = () => {
    const dataPath = path.join(__dirname, "data", "historial.json")
    const contenido = fs.readFileSync(dataPath, "utf-8")
    return JSON.parse(contenido)
}

const crearTablaHistorial = historial => {
    return historial.map(reserva => `
    <tr class="border-b border-slate-100 hover:bg-slate-50 transition">
      <td class="p-3 text-slate-700">${reserva.sala}</td>
      <td class="p-3 text-slate-600">${reserva.fecha}</td>
      <td class="p-3 text-slate-600">${reserva.hora}</td>
    </tr>
  `).join('');
}

const leerHistorial = nombreUsuario => {
    const contenido = leerJson()
    const filtrado = contenido.filter(reserva => reserva.nombreUsuario === nombreUsuario)
    return crearTablaHistorial(filtrado)
}

const agregarHistorial = nuevaReserva => {
    const contenido = leerJson()
    contenido.push(nuevaReserva)
    const dataPath = path.join(__dirname, "data", "historial.json")
    fs.writeFileSync(dataPath, JSON.stringify(contenido, null, 2), "utf-8")
}

module.exports = {leerHistorial, agregarHistorial}
