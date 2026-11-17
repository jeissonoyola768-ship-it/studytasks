# 📚 StudyTasks – Entrega 1

Gestor de tareas académicas (API REST + interfaz web) construido con **Flask** y empaquetado en **Docker**.
Proyecto de aula · SD1005 Sistemas Operativos · 2026-II.

## ¿Qué problema resuelve?
Los estudiantes manejan varias materias con fechas de entrega distintas y suelen perder el control de lo pendiente.
StudyTasks permite registrar, ordenar por fecha límite, completar y eliminar tareas desde el navegador.

## Requisitos
- [Docker](https://docs.docker.com/get-docker/) instalado y en ejecución. No se necesita Python ni nada más.

## Construir y ejecutar (Entrega 1)

```bash
# 1. Clonar el repositorio
git clone <URL-DEL-REPOSITORIO>
cd studytasks

# 2. Construir la imagen a partir del Dockerfile
docker build -t studytasks:1.0 .

# 3. Ejecutar el contenedor publicando el puerto 5000
docker run -d --name studytasks -p 5000:5000 studytasks:1.0

# 4. Abrir en el navegador
#    http://localhost:5000
```

### Verificar
```bash
docker images                 # la imagen studytasks:1.0
docker ps                     # el contenedor en ejecución (STATUS: Up ... healthy)
docker logs studytasks        # registros de gunicorn
curl http://localhost:5000/health
curl http://localhost:5000/api/tareas
```

### Detener y limpiar
```bash
docker stop studytasks
docker rm studytasks
docker rmi studytasks:1.0
```

> ⚠️ En la Entrega 1 los datos se guardan en SQLite **dentro** del contenedor: si lo eliminas con `docker rm`, se pierden.
> Esto se resuelve en la Entrega 2 con PostgreSQL y un volumen.

## API
| Método | Ruta | Descripción |
|---|---|---|
| GET | `/` | Interfaz web |
| GET | `/health` | Estado del servicio |
| GET | `/api/info` | Versión, contenedor y base de datos |
| GET | `/api/tareas` | Lista las tareas |
| POST | `/api/tareas` | Crea tarea `{"titulo","materia","fecha_limite":"AAAA-MM-DD"}` |
| PATCH | `/api/tareas/<id>` | Alterna completada / pendiente |
| DELETE | `/api/tareas/<id>` | Elimina la tarea |

## Estructura
```
studytasks/
├── app/               # código de la aplicación (Flask)
├── tests/             # pruebas automáticas
├── docs/              # diagrama y PDF de la entrega
├── Dockerfile         # receta de la imagen
├── requirements.txt
└── README.md
```

## Pruebas (opcional, sin Docker)
```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
```
