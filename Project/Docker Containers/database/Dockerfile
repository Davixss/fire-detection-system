# Utilizza un'immagine base di Python
FROM python:3.9

# Aggiorna il sistema e installa dipendenze necessarie
RUN apt-get update && apt-get install -y \
    build-essential \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Installa i servizi
RUN pip install mysql-connector-python Flask
RUN apt-get update && apt-get install -y net-tools iputils-ping lsof default-mysql-client

# Imposta la directory di lavoro
WORKDIR /app

# Copia il contenuto della directory corrente nel container
COPY app/ /app/

# Espone la porta su cui Flask sarà in ascolto
EXPOSE 5050 

# Imposta lo script di entrypoint
CMD ["python", "/app/server.py"]
