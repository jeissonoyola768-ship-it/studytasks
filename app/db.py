"""Capa de datos de StudyTasks.

- Si existe la variable DB_HOST  -> PostgreSQL (Docker Compose, Entrega 2).
- Si no existe                   -> SQLite local (Entrega 1 / pruebas).
Toda la configuración llega por variables de entorno.
"""
import os
import sqlite3
import time
from datetime import datetime

DB_HOST = os.getenv("DB_HOST")
USE_PG = bool(DB_HOST)
SQLITE_PATH = os.getenv("SQLITE_PATH", "tareas.db")

if USE_PG:
    import psycopg2
    from psycopg2.extras import RealDictCursor

DDL_PG = """
CREATE TABLE IF NOT EXISTS tareas (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(120) NOT NULL,
    materia VARCHAR(80) NOT NULL DEFAULT 'General',
    fecha_limite VARCHAR(10),
    completada SMALLINT NOT NULL DEFAULT 0,
    creada_en VARCHAR(19) NOT NULL
)"""

DDL_SQLITE = """
CREATE TABLE IF NOT EXISTS tareas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    materia TEXT NOT NULL DEFAULT 'General',
    fecha_limite TEXT,
    completada INTEGER NOT NULL DEFAULT 0,
    creada_en TEXT NOT NULL
)"""


def backend():
    return "postgresql" if USE_PG else "sqlite"


def _connect_pg(intentos, espera=2):
    """Conecta a PostgreSQL; reintenta por si la BD aún está arrancando."""
    ultimo_error = None
    for n in range(1, intentos + 1):
        try:
            return psycopg2.connect(
                host=DB_HOST,
                port=os.getenv("DB_PORT", "5432"),
                dbname=os.environ["DB_NAME"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"],
                connect_timeout=5,
            )
        except psycopg2.OperationalError as exc:
            ultimo_error = exc
            print(f"[db] intento {n}/{intentos}: PostgreSQL no disponible, reintentando...", flush=True)
            if n < intentos:
                time.sleep(espera)
    raise ultimo_error


def _run(sql, params=(), fetch="none", intentos=1):
    """Ejecuta una sentencia. El SQL usa %s como marcador en ambos motores."""
    if USE_PG:
        conn = _connect_pg(intentos)
        try:
            with conn:  # commit / rollback automático
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(sql, params)
                    rows = [dict(r) for r in cur.fetchall()] if fetch != "none" else []
        finally:
            conn.close()
    else:
        conn = sqlite3.connect(SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        try:
            cur = conn.execute(sql.replace("%s", "?"), params)
            rows = [dict(r) for r in cur.fetchall()] if fetch != "none" else []
            conn.commit()
        finally:
            conn.close()
    if fetch == "one":
        return rows[0] if rows else None
    return rows


def init_db():
    _run(DDL_PG if USE_PG else DDL_SQLITE, intentos=30)


def ping():
    _run("SELECT 1", fetch="all")


def listar():
    return _run(
        "SELECT * FROM tareas ORDER BY completada, "
        "COALESCE(fecha_limite, '9999-12-31'), id",
        fetch="all",
    )


def crear(titulo, materia, fecha_limite):
    return _run(
        "INSERT INTO tareas (titulo, materia, fecha_limite, creada_en) "
        "VALUES (%s, %s, %s, %s) RETURNING *",
        (titulo, materia, fecha_limite, datetime.now().isoformat(timespec="seconds")),
        fetch="one",
    )


def alternar(tarea_id):
    return _run(
        "UPDATE tareas SET completada = 1 - completada WHERE id = %s RETURNING *",
        (tarea_id,),
        fetch="one",
    )


def eliminar(tarea_id):
    row = _run("DELETE FROM tareas WHERE id = %s RETURNING id", (tarea_id,), fetch="one")
    return row is not None
