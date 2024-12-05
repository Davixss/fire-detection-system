# Server Flask ORCHESTRATOR

from classes.Routes import *
from classes.FlaskConfig import *
from flask import Flask, request, redirect, url_for, jsonify

app = Flask(__name__)


# Sensor API Routing
@app.route('/sensor', methods=['GET'])
def getSensor():
    return SensorAPI.get(request.args)
@app.route('/sensor', methods=['POST'])
def postSensor():
    return SensorAPI.post(request.get_json())
@app.route('/sensor', methods=['PUT'])
def putSensor():
    return SensorAPI.put(request.get_json())
@app.route('/sensor', methods=['DELETE'])
def deleteSensor():
    return SensorAPI.delete(request.args)


# Sensor API Routing
@app.route('/actuator', methods=['GET'])
def getActuator():
    return ActuatorAPI.get(request.args)
@app.route('/actuator', methods=['POST'])
def postActuator():
    return ActuatorAPI.post(request.get_json())
@app.route('/actuator', methods=['PUT'])
def putActuator():
    return ActuatorAPI.put(request.get_json())
@app.route('/actuator', methods=['DELETE'])
def deleteActuator():
    return ActuatorAPI.delete(request.args)


@app.route('/device_event', methods=['GET'])
def getDeviceEvent():
    return DeviceEventAPI.get(request.args)
@app.route('/device_event', methods=['POST'])
def postDeviceEvent():
    return DeviceEventAPI.post(request.get_json())
@app.route('/device_event', methods=['PUT'])
def putDeviceEvent():
    return DeviceEventAPI.put(request.get_json())
@app.route('/device_event', methods=['DELETE'])
def deleteDeviceEvent():
    return DeviceEventAPI.delete(request.args)


@app.route('/actuator_based_on_event', methods=['GET'])
def getActuatorBasedOnEvent():
    return ActuatorAPI.getBasedOnEvent(request.args)


# Start Flask Server
if __name__ == '__main__':
    app.run(host=ThisServer.FLASK_HOST, port=ThisServer.FLASK_PORT, debug=True)