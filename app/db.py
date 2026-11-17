"""Capa de datos de StudyTasks (Entrega 1: SQLite dentro del contenedor)."""
import os
import sqlite3
from datetime import datetime

DB_PATH = os.getenv("SQLITE_PATH", "tareas.db")


def backend():
    return "sqlite"


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _run(sql, params=(), fetch="none"):
    conn = _connect()
    try:
        cur = conn.execute(sql, params)
        rows = cur.fetchall() if fetch in ("all", "one") else []
        conn.commit()
    finally:
        conn.close()
    rows = [dict(r) for r in rows]
    if fetch == "one":
        return rows[0] if rows else None
    return rows


def init_db():
    _run(
        """CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            materia TEXT NOT NULL DEFAULT 'General',
            fecha_limite TEXT,
            completada INTEGER NOT NULL DEFAULT 0,
            creada_en TEXT NOT NULL
        )"""
    )


def ping():
    _run("SELECT 1")


def listar():
    return _run(
        "SELECT * FROM tareas ORDER BY completada, "
        "COALESCE(fecha_limite, '9999-12-31'), id",
        fetch="all",
    )


def crear(titulo, materia, fecha_limite):
    return _run(
        "INSERT INTO tareas (titulo, materia, fecha_limite, creada_en) "
        "VALUES (?, ?, ?, ?) RETURNING *",
        (titulo, materia, fecha_limite, datetime.now().isoformat(timespec="seconds")),
        fetch="one",
    )


def alternar(tarea_id):
    return _run(
        "UPDATE tareas SET completada = 1 - completada WHERE id = ? RETURNING *",
        (tarea_id,),
        fetch="one",
    )


def eliminar(tarea_id):
    row = _run("DELETE FROM tareas WHERE id = ? RETURNING id", (tarea_id,), fetch="one")
    return row is not None
