const fs = require("fs");
const path = require("path");

const getJson = () => {
    const dataPath = path.join(__dirname, "data", "salas.json")
    const string = fs.readFileSync(dataPath, "utf8");
    return JSON.parse(string)
}

const getSalas = () => {
    const json = getJson()
    // Asegúrate de enviar también el id de la sala para poder usarlo al redirigir
    return json.map(sala => ({"id": sala.id, "nombre": sala.nombre}))
}

const getSalaDetalles = idSala => {
    const json = getJson()
    return json.filter(sala => sala.id === idSala)
}

const putReservado = (idSala, horaInicio) => {
    const json = getJson();
    
    const sala = json.find(s => s.id === idSala);
    if (sala) {
        const horario = sala.horarios.find(h => h.hora_inicio === horaInicio);
        if (horario) horario.reservada = true;
    }
    fs.writeFileSync(path.join(__dirname, "data", "salas.json"), JSON.stringify(json, null, 2));

}

module.exports = {getSalas, getSalaDetalles, putReservado}