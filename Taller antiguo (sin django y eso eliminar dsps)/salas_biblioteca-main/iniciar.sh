#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if ! command -v npm >/dev/null 2>&1; then
  echo "Error: npm no esta instalado o no esta en PATH."
  exit 1
fi

echo "Iniciando backend con npm run dev..."
npm run dev > /tmp/salas_biblioteca_backend.log 2>&1 &
BACKEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Esperando 3 segundos para abrir el navegador..."
sleep 3

URL="http://localhost:3000/index.html"

if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$URL" >/dev/null 2>&1 || true
elif command -v open >/dev/null 2>&1; then
  open "$URL" >/dev/null 2>&1 || true
else
  echo "No se encontro comando para abrir navegador automaticamente."
  echo "Abre manualmente: $URL"
fi

echo "Listo. Para detener el backend, usa: kill $BACKEND_PID"
