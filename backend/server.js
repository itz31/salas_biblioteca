const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const port = process.env.PORT || 3000;
const backendDir = __dirname;
const frontendDir = path.join(__dirname, '..', 'frontend');
const dataPath = path.join(backendDir, 'data', 'perfiles.json');

app.use(express.json());
app.use(express.static(frontendDir));

function leerPerfiles() {
  const contenido = fs.readFileSync(dataPath, 'utf8');
  return JSON.parse(contenido);
}

function guardarPerfiles(data) {
  fs.writeFileSync(dataPath, JSON.stringify(data, null, 2), 'utf8');
}

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

function obtenerListaPorTipo(data, tipo) {
  return tipo === 'estudiante' ? data.estudiantes : data.funcionarios;
}

function obtenerSiguienteId(lista, prefijo) {
  const maxNumero = lista.reduce((maximo, perfil) => {
    const numero = Number.parseInt(String(perfil.id || '').replace(/^[^0-9]*/, ''), 10);
    return Number.isFinite(numero) && numero > maximo ? numero : maximo;
  }, 0);

  return `${prefijo}${String(maxNumero + 1).padStart(3, '0')}`;
}

app.get('/', function (_request, response) {
  response.redirect('/login.html');
});

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
  const perfil = lista.find(function (usuario) {
    return usuario.correo.toLowerCase() === correo.toLowerCase() && usuario.password === password;
  });

  if (!perfil) {
    return response.status(401).json({ mensaje: 'Correo o contraseña incorrectos.' });
  }

  const { password: _password, ...perfilSinPassword } = perfil;
  return response.json({ perfil: perfilSinPassword });
});

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

app.listen(port, function () {
  console.log(`Servidor listo en http://localhost:${port}`);
});