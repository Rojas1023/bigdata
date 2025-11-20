# Imagen base ligera
FROM python:3.10-slim

# Evitar preguntas interactivas
ENV PYTHONUNBUFFERED=1

# Crear carpeta de la app
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Exponer puerto del container
EXPOSE 8000

# Comando para iniciar Flask con Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app.main:app"]
