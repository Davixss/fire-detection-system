# Configurazione delle reti IP:Porta dei containers Docker
# ThisServer deve ascoltare su '0.0.0.0' 

class ThisServer:
    FLASK_HOST = '0.0.0.0'
    FLASK_PORT = 5000

class ServerProxy:
    FLASK_HOST = '10.24.104.16'
    FLASK_PORT = 7070