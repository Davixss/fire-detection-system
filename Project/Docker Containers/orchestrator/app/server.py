# Server Flask ORCHESTRATOR

from classes.Routes import *
from classes.FlaskConfig import *
from flask import Flask, request, redirect, url_for, jsonify

app = Flask(__name__)


# Sensor API Routing
@app.route('/orchestrator/sensor', methods=['GET'])
def getSensor():
    return SensorAPI.get(request.args, request.remote_addr)

# Sensor API Routing
@app.route('/orchestrator/actuator', methods=['GET'])
def getActuator():
    return ActuatorAPI.get(request.args, request.remote_addr)

@app.route('/orchestrator/actuator_based_on_event', methods=['GET'])
def getActuatorBasedOnEvent():
    return ActuatorAPI.getBasedOnEvent(request.args, request.remote_addr)


# Start Flask Server
if __name__ == '__main__':
    app.run(host=ThisServer.FLASK_HOST, port=ThisServer.FLASK_PORT, debug=True)