# Se utiliza una imagen de Python 3.9 como base
FROM python:3.9-slim

# Se establece el directorio de trabajo
WORKDIR /app

# Se copian los archivos necesarios en el contenedor
COPY requirements.txt .
COPY app.py .
COPY dataupload.py .
COPY klines_BTCUSDT_5m.csv .

# Se instalan las dependencias especificadas en el archivo requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Se establece el comando para ejecutar los archivos Python de forma continua cada 5 minutos
CMD ["sh", "-c", "while true; do python3 app.py && sleep 300; done"]
CMD ["sh", "-c", "while true; do python3 dataupload.py && sleep 300; done"]
