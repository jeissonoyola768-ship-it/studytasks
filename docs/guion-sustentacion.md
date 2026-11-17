# Guion de sustentación en vivo (Entrega 2)

Duración sugerida: 8–10 minutos. Todos los integrantes deben poder explicar cada paso.

## 0. Antes de entrar al salón
- [ ] Docker Desktop abierto y funcionando (`docker version`).
- [ ] Repositorio clonado y `.env` creado desde `.env.example`.
- [ ] Imágenes ya descargadas (`docker compose pull` y `docker compose build`) por si falla el internet.
- [ ] Estado limpio: `docker compose down -v` para empezar desde cero.

## 1. Arquitectura (1–2 min)
Mostrar `docs/arquitectura-entrega2.png` y explicar: usuario → puerto 5000 → `web` → red `backend` → `db` → volumen `pgdata`.

## 2. Levantar el proyecto (2 min)
```bash
docker compose up -d --build
docker compose ps
docker compose logs --tail 20 web
```
Explicar: `--build` construye nuestra imagen con el Dockerfile; `-d` segundo plano; `depends_on` + healthcheck.

## 3. Comunicación entre servicios (2 min)
```bash
curl http://localhost:5000/api/info
docker network inspect studytasks_backend
docker compose exec web getent hosts db
docker compose exec db psql -U studytasks -d studytasks -c "SELECT * FROM tareas;"
```
Explicar: el nombre del servicio (`db`) funciona como DNS dentro de la red; la BD no publica puertos.

## 4. Persistencia (2 min)
1. Crear 2 tareas en la web.
2. `docker compose down` → mostrar `docker volume ls` (el volumen sigue).
3. `docker compose up -d` → recargar la página: las tareas siguen.
4. Contraste con Entrega 1: en SQLite sin volumen se pierden al borrar el contenedor.

## 5. Ciclo de vida (1 min)
```bash
docker compose stop && docker compose start
docker compose restart web
docker compose logs -f web
```

## Preguntas frecuentes del profesor
| Pregunta | Respuesta corta |
|---|---|
| ¿Diferencia entre imagen y contenedor? | Imagen = plantilla inmutable por capas; contenedor = instancia en ejecución con capa de escritura. |
| ¿Por qué no usar la BD sin volumen? | La capa del contenedor es efímera; `down` la elimina. |
| ¿Qué hace `down` vs `down -v`? | `down` borra contenedores y red; `-v` borra además los volúmenes. |
| ¿Por qué `web` usa `db` como host? | Compose crea una red y un DNS interno con el nombre de cada servicio. |
| ¿Cómo evita subir secretos? | `.env` en `.gitignore`; solo se sube `.env.example`. |
| ¿Qué es el healthcheck? | `pg_isready` marca `db` como healthy; `web` espera esa condición. |
| ¿Es un contenedor una máquina virtual? | No: comparte el kernel del anfitrión y se aísla con namespaces y cgroups. |
| ¿Por qué se copia requirements.txt antes del código? | Para reutilizar la caché de capas al cambiar solo el código. |
| ¿Qué pasa si cambio el puerto? | Cambio `APP_PORT` en `.env`; el puerto interno sigue siendo 5000. |
