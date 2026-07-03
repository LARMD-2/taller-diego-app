# Usamos una imagen ligera de Python 3.11
FROM python:3.11-slim

# Configuraciones de entorno estándar
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/backend

# Directorio de trabajo
WORKDIR /app

# Instalamos dependencias primero (aprovechando caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copiamos todo el código fuente
COPY . .

# Exponemos el puerto
EXPOSE 8000

# Comando de inicio
CMD ["sh", "-c", "sleep 5 && uvicorn backend.main:app --host 0.0.0.0 --port 8000"]