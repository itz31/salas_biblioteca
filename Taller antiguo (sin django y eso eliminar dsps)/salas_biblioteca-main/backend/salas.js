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
    const idLimpio = idSala.replace('S-', '').replace(/^0+/, ''); // "S-006" → "6"
    const json = getJson();
    const sala = json[idLimpio];
    if (!sala) return [];

    const dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes'];
    const diasNombre = { lunes: 'Lunes', martes: 'Martes', miercoles: 'Miércoles', jueves: 'Jueves', viernes: 'Viernes' };

    // Expandir cada bloque × cada día en un horario individual
    const horarios = [];
    sala.disponibilidad.forEach(bloque => {
        const [hora_inicio, hora_fin] = bloque.bloque.split(' - ');
        dias.forEach(dia => {
            horarios.push({
                dia: diasNombre[dia],
                hora_inicio: hora_inicio.trim(),
                hora_finalizacion: hora_fin.trim(),
                reservada: !bloque[dia]   // true en json = disponible, false = reservado
            });
        });
    });

    const salaTransformada = {
        id: `S-${sala.numero.toString().padStart(3, '0')}`,
        nombre: `Sala ${sala.numero}`,
        piso: sala.piso,
        capacidad: sala.capacidad,
        sillas: sala.sillas,
        pizarra: sala.pizarra,         // "Grande", "Pequeña", "Mediana"
        multimedia: sala.television !== "No tiene",
        entorno: sala.vista,
        horarios
    };

    return [salaTransformada];
};

const putReservado = (idSala, horaInicio, dia) => {
    const idLimpio = idSala.replace('S-', '').replace(/^0+/, '');
    const json = getJson();
    const sala = json[idLimpio];
    if (!sala) return false;

    const diaKey = dia.toLowerCase()
        .replace('é', 'e').replace('á', 'a'); // "Miércoles" → "miercoles"

    const bloque = sala.disponibilidad.find(d => d.bloque.startsWith(horaInicio));
    if (bloque) {
        bloque[diaKey] = false; // marcar como reservado
    }

    fs.writeFileSync(path.join(__dirname, "data", "salas.json"), JSON.stringify(json, null, 2));
    return true;
};

module.exports = {getSalas, getSalaDetalles, putReservado}