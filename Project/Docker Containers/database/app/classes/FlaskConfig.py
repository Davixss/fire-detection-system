# Configurazione delle reti IP:Porta dei containers Docker
# ThisServer deve ascoltare su '0.0.0.0' 

class ThisServer:
    FLASK_HOST = '0.0.0.0'
    FLASK_PORT = 5050

class Controller:
    FLASK_HOST = 'IP_EDOARDO'
    FLASK_PORT = 6060