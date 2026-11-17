"""StudyTasks - gestor de tareas académicas (API REST + interfaz web)."""
import os
import re
import socket

from flask import Flask, jsonify, render_template, request

import db

VERSION = "2.0.0"
FECHA_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

app = Flask(__name__)
db.init_db()


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    try:
        db.ping()
        return jsonify(status="ok", db=db.backend())
    except Exception as exc:  # noqa: BLE001
        return jsonify(status="error", detail=str(exc)), 503


@app.get("/api/info")
def info():
    return jsonify(
        app="StudyTasks",
        version=VERSION,
        contenedor=socket.gethostname(),
        base_de_datos=db.backend(),
        entorno=os.getenv("APP_ENV", "dev"),
    )


@app.get("/api/tareas")
def listar():
    return jsonify(db.listar())


@app.post("/api/tareas")
def crear():
    datos = request.get_json(silent=True) or {}
    titulo = (datos.get("titulo") or "").strip()
    materia = (datos.get("materia") or "General").strip() or "General"
    fecha = (datos.get("fecha_limite") or "").strip() or None
    if not titulo:
        return jsonify(error="El título es obligatorio"), 400
    if len(titulo) > 120:
        return jsonify(error="El título supera 120 caracteres"), 400
    if fecha and not FECHA_RE.match(fecha):
        return jsonify(error="La fecha debe tener formato AAAA-MM-DD"), 400
    return jsonify(db.crear(titulo, materia, fecha)), 201


@app.patch("/api/tareas/<int:tarea_id>")
def alternar(tarea_id):
    tarea = db.alternar(tarea_id)
    if tarea is None:
        return jsonify(error="Tarea no encontrada"), 404
    return jsonify(tarea)


@app.delete("/api/tareas/<int:tarea_id>")
def eliminar(tarea_id):
    if not db.eliminar(tarea_id):
        return jsonify(error="Tarea no encontrada"), 404
    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
