#!/usr/bin/env bash
# Demuestra la persistencia: crea una tarea, destruye y recrea los contenedores
# (SIN borrar el volumen) y comprueba que la tarea sigue ahí.
set -euo pipefail
PORT="${APP_PORT:-5000}"
URL="http://localhost:${PORT}"

echo "1) Levantando servicios..."
docker compose up -d --build
until curl -fs "$URL/health" >/dev/null; do sleep 2; done

echo "2) Creando una tarea de prueba..."
curl -s -X POST "$URL/api/tareas" -H "Content-Type: application/json" \
  -d '{"titulo":"Tarea que debe persistir","materia":"Sistemas Operativos","fecha_limite":"2026-12-01"}'
echo; echo "Tareas antes:"; curl -s "$URL/api/tareas"; echo

echo "3) Eliminando contenedores y red (el volumen se conserva)..."
docker compose down
docker volume ls | grep pgdata

echo "4) Recreando contenedores..."
docker compose up -d
until curl -fs "$URL/health" >/dev/null; do sleep 2; done

echo "5) Tareas despues (deben ser las mismas):"
curl -s "$URL/api/tareas"; echo
