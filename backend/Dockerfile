# Dockerfile para despliegue en Render (FastAPI)

FROM python:3.11-slim

WORKDIR /workspace

# Instalar dependencias del sistema necesarias si es necesario
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del backend
COPY app/ ./app/

# Exponer el puerto por defecto (Render inyecta PORT dinámicamente)
EXPOSE 8000

# Ejecutar la aplicación con uvicorn, leyendo el puerto de la variable de entorno PORT (default 8000)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
