# Utilizza un'immagine base di Python
FROM python:3.9

# Aggiorna il sistema e installa dipendenze necessarie
RUN apt-get update && apt-get install -y \
    apache2 \
    libapache2-mod-php \
    php \
    php-mysqli \
    build-essential \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Installa i servizi
RUN pip install mysql-connector-python AWSIoTPythonSDK geopy colorama
RUN apt-get update && apt-get install -y net-tools iputils-ping lsof default-mysql-client

# Abilita il modulo di riscrittura Apache (opzionale, utile per PHP)
RUN a2enmod rewrite

WORKDIR /app

COPY app/app /app/
COPY app/webgui/ /var/www/html/

# Imposta i permessi per Apache e Flask
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html \
    && chmod -R 755 /app

EXPOSE 8181

# Avvia sia Apache che Flask
CMD ["bash", "-c", "service apache2 start && python /app/actuator.py"]
