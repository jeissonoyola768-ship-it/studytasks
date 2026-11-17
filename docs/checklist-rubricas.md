# Verificación contra las rúbricas

## Entrega 1 (5,0)
| Criterio | Pts | Dónde se cumple |
|---|---|---|
| Planteamiento del problema | 0,7 | PDF Entrega 1, sección 1 |
| Solución y esquema de desarrollo | 0,7 | PDF sección 2 y 3 + `docs/arquitectura-entrega1.png` |
| Primera versión funcional y código organizado | 0,7 | `app/`, `tests/` |
| Dockerfile propio | 1,0 | `Dockerfile` (base, dependencias, WORKDIR, CMD) |
| Construcción y ejecución | 1,0 | `docker build` / `docker run` (capturas 1–6) |
| GitHub, README y evidencias | 0,5 | Repositorio, `README.md`, PDF sección 8 |
| Conceptos y comandos Docker | 0,4 | PDF sección 6 y 7 |

## Entrega 2 (5,0)
| Criterio | Pts | Dónde se cumple |
|---|---|---|
| Funcionamiento de la app y servicios | 1,0 | `web` + `db` con `docker compose up -d` |
| Docker Compose correcto | 1,0 | `compose.yaml` (build, depends_on+healthcheck, restart) |
| Red y comunicación | 0,7 | red `backend`, host `db`, BD sin puertos publicados |
| Volúmenes y persistencia | 0,8 | volumen `pgdata`; `scripts/demo_persistencia.sh` |
| Variables de entorno | 0,4 | `.env.example`, `.gitignore`, `${VAR}` en Compose |
| Documentación y reproducibilidad | 0,5 | `README.md`, esquema actualizado, PDF final |
| Sustentación y demostración | 0,6 | `docs/guion-sustentacion.md` |

## Condiciones de validación
- [x] Imagen propia construida con Dockerfile (no solo imágenes públicas).
- [x] README permite reproducir en otro computador con Docker.
- [ ] Todos los integrantes pueden explicar la solución.
- [ ] El proyecto se ejecuta en vivo (las capturas no lo reemplazan).
