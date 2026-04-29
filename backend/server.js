const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const port = process.env.PORT || 3000;
const backendDir = __dirname;
const frontendDir = path.join(__dirname, '..', 'frontend');
const dataPath = path.join(backendDir, 'data', 'perfiles.json');
const reservasModule = require("./reservas");
const historialModule = require("./historial");
const salasModule = require("./salas");


app.use(express.json());
app.use(express.static(frontendDir));

/**
 * Lee el archivo de perfiles y lo devuelve como objeto JS.
 * Reutilizar cuando necesites el estado actual de usuarios.
 */
function leerPerfiles() {
  const contenido = fs.readFileSync(dataPath, 'utf8');
  return JSON.parse(contenido);
}

/**
 * Guarda en disco el objeto completo de perfiles.
 * Reutilizar despues de crear o modificar usuarios.
 */
function guardarPerfiles(data) {
  fs.writeFileSync(dataPath, JSON.stringify(data, null, 2), 'utf8');
}

/**
 * Detecta si un correo pertenece a estudiante o funcionario segun el dominio.
 * Devuelve 'estudiante', 'funcionario' o null si no coincide.
 */
function detectarTipo(correo, reglas) {
  const correoNormalizado = correo.toLowerCase();

  if (correoNormalizado.endsWith(reglas.estudiante)) {
    return 'estudiante';
  }

  if (correoNormalizado.endsWith(reglas.funcionario)) {
    return 'funcionario';
  }

  return null;
}

/**
 * Retorna la lista correcta segun el tipo de usuario.
 * Si tipo es 'estudiante' devuelve data.estudiantes, si no data.funcionarios.
 */
function obtenerListaPorTipo(data, tipo) {
  return tipo === 'estudiante' ? data.estudiantes : data.funcionarios;
}

/**
 * Calcula el siguiente ID disponible usando un prefijo (E o F).
 * Ejemplo: E004 -> E005.
 */
function obtenerSiguienteId(lista, prefijo) {
  const maxNumero = lista.reduce((maximo, perfil) => {
    const numero = Number.parseInt(String(perfil.id || '').replace(/^[^0-9]*/, ''), 10);
    return Number.isFinite(numero) && numero > maximo ? numero : maximo;
  }, 0);

  return `${prefijo}${String(maxNumero + 1).padStart(3, '0')}`;
}

/**
 * Endpoint de login:
 * valida datos, busca al usuario y devuelve el perfil sin password.
 */
app.post('/api/login', function (request, response) {
  const { correo, password } = request.body || {};

  if (!correo || !password) {
    return response.status(400).json({ mensaje: 'Debes ingresar correo y contraseña.' });
  }

  const data = leerPerfiles();
  const tipo = detectarTipo(correo, data.reglasClasificacion);

  if (!tipo) {
    return response.status(400).json({ mensaje: 'El correo debe terminar en @alumnos.ucn.cl o @funcionario.ucn.cl.' });
  }

  const lista = obtenerListaPorTipo(data, tipo);
  // Busca coincidencia exacta de correo+password en el grupo correspondiente.
  const perfil = lista.find(function (usuario) {
    return usuario.correo.toLowerCase() === correo.toLowerCase() && usuario.password === password;
  });

  if (!perfil) {
    return response.status(401).json({ mensaje: 'Correo o contraseña incorrectos.' });
  }

  const { password: _password, ...perfilSinPassword } = perfil;
  return response.json({ perfil: perfilSinPassword });
});

/**
 * Endpoint de registro:
 * crea un usuario nuevo en la lista correcta y persiste cambios en JSON.
 */
app.post('/api/register', function (request, response) {
  const { nombre, correo, password } = request.body || {};

  if (!nombre || !correo || !password) {
    return response.status(400).json({ mensaje: 'Debes ingresar nombre, correo y contraseña.' });
  }

  const data = leerPerfiles();
  const tipo = detectarTipo(correo, data.reglasClasificacion);

  if (!tipo) {
    return response.status(400).json({ mensaje: 'El correo debe terminar en @alumnos.ucn.cl o @funcionario.ucn.cl.' });
  }

  const lista = obtenerListaPorTipo(data, tipo);
  const correoNormalizado = correo.toLowerCase();
  // Evita registrar correos duplicados dentro del mismo tipo de usuario.
  const existe = lista.some(function (usuario) {
    return usuario.correo.toLowerCase() === correoNormalizado;
  });

  if (existe) {
    return response.status(409).json({ mensaje: 'Ese correo ya está registrado.' });
  }

  const prefijo = tipo === 'estudiante' ? 'E' : 'F';
  const nuevoPerfil = {
    id: obtenerSiguienteId(lista, prefijo),
    nombre: nombre.trim(),
    correo: correoNormalizado,
    tipo,
    password
  };

  lista.push(nuevoPerfil);
  guardarPerfiles(data);

  const { password: _password, ...perfilSinPassword } = nuevoPerfil;
  return response.status(201).json({ perfil: perfilSinPassword });
});

app.get("/reservas/:param?", (request, response) => {
  return response.status(200).json({ html: reservasModule.listReservas(request.params.param) });
});

app.get("/reservas/all", (request, response) => {
  return response.status(200).json({ html: reservasModule.listAllReservas() });
})

app.get("/historial/:param?", (request, response) => {
  return response.status(200).json({ html: historialModule.leerHistorial(request.params.param) });
})

app.delete("/reservas/:param?", (request, response) => {
  reservasModule.eliminarReserva(request.params.param);
  return response.status(200).json({ mensaje: `exito eliminacion reserva id ${request.params.param}` });
});

app.post("/reservas", (request, response) => {
  const nuevaReserva = request.body;
  if (!nuevaReserva) {
    return response.status(400).json({ mensaje: "Faltan datos de la reserva." });
  }
  reservasModule.crearReserva(nuevaReserva);
  historialModule.agregarHistorial(nuevaReserva);
  return response.status(201).json({ mensaje: "Reserva creada con éxito" });
});

app.get("/salas", (request, response) => {
  return response.status(200).json(salasModule.getSalas());
})

app.get("/salas/:param?", (request, response) => {
  return response.status(200).json(salasModule.getSalaDetalles(request.params.param));
})



app.put("/salas/:param?", (request, response) => {
  const id = request.params.param.split(",")[0];
  const hora = request.params.param.split(",")[1];
  const { dia } = request.body;
  salasModule.putReservado(id, hora, dia)
  return response.status(200).json({mensaje: "se ha reservado con exito"})
})
/**
 * Inicia el servidor HTTP en el puerto configurado.
 */
app.listen(port, function () {
  console.log(`Servidor listo en http://localhost:${port}`);
});
