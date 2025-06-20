# Usa Python 3.10 oficial
FROM python:3.10-slim

# Variables de entorno para evitar buffering y habilitar logs
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY . .

# Instala las dependencias del sistema base
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala las dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expone el puerto usado por Uvicorn (interno al contenedor)
EXPOSE 8080

# Comando por defecto para ejecutar FastAPI con recarga (modo desarrollo)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
