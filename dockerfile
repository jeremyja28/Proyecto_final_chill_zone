# Usa una imagen oficial de Python como base
FROM python:3.12-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requerimientos desde la subcarpeta
COPY SGCZ-ChillZone/requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación desde la subcarpeta
COPY SGCZ-ChillZone/ .

# Expone el puerto correcto
EXPOSE 4000

# Define la variable de entorno para el puerto
ENV PORT=4000

# Comando por defecto para correr la aplicación
CMD ["python", "app.py"]
#frvgfv