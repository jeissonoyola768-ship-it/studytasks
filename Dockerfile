# ---- Imagen base ligera de Python ----
FROM python:3.12-slim

# Python sin .pyc y con logs sin buffer (se ven en `docker logs`)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Directorio de trabajo dentro de la imagen
WORKDIR /app

# Dependencias primero: aprovecha la caché de capas de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código de la aplicación
COPY app/ ./

# Usuario sin privilegios (buena práctica de seguridad)
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

# Documenta el puerto en el que escucha la aplicación
EXPOSE 5000

# Comprobación de salud del contenedor
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Comando de inicio: servidor de producción gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
