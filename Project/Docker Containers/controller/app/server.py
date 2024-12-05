# Server Flask ORCHESTRATOR

from classes.Routes import *
from classes.FlaskConfig import *
from flask import Flask, request

app = Flask(__name__)


# Sensor API Routing
@app.route('/controller/sensor', methods=['GET'])
def getSensor():
    return SensorAPI.get(request.args, request.remote_addr)
@app.route('/controller/sensor', methods=['POST'])
def postSensor():
    return SensorAPI.post(request.get_json(),request.remote_addr)
@app.route('/controller/sensor', methods=['PUT'])
def putSensor():
    return SensorAPI.put(request.get_json(),request.remote_addr)
@app.route('/controller/sensor', methods=['DELETE'])
def deleteSensor():
    return SensorAPI.delete(request.args,request.remote_addr)


# Sensor API Routing
@app.route('/controller/actuator', methods=['GET'])
def getActuator():
    return ActuatorAPI.get(request.args,request.remote_addr)
@app.route('/controller/actuator', methods=['POST'])
def postActuator():
    return ActuatorAPI.post(request.get_json(),request.remote_addr)
@app.route('/controller/actuator', methods=['PUT'])
def putActuator():
    return ActuatorAPI.put(request.get_json(),request.remote_addr)
@app.route('/controller/actuator', methods=['DELETE'])
def deleteActuator():
    return ActuatorAPI.delete(request.args,request.remote_addr)


@app.route('/controller/log', methods=['POST'])
def postLog():
    return Logs.post(request.get_json(),request.remote_addr)


# Start Flask Server
if __name__ == '__main__':
    app.run(host=ThisServer.FLASK_HOST, port=ThisServer.FLASK_PORT, debug=True)