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
RUN pip install nginx
RUN apt-get update && apt-get install -y net-tools iputils-ping lsof

# Imposta la directory di lavoro
WORKDIR /app

# Espone la porta su cui Flask sarà in ascolto
EXPOSE 7070 
