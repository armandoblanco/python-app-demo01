# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los archivos necesarios al contenedor
COPY requirements.txt requirements.txt
COPY . .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Definir variable de entorno para la cadena de conexión SQL (ejemplo PostgreSQL)
ENV DATABASE_URL="postgresql://admin:password01@host:5432/master"

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]