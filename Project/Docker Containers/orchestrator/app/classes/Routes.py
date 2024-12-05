# Server Flask DATABASE
# Per ricevere le richieste da parte di controller/orchestrator

from classes.Database import *
from classes.Functions import *
from flask import jsonify


# Istanza del database per effettuare le query 
db = Database()


# Class Sensor API Routes
class SensorAPI:
    def get(data, ipAddress):
        ipAddressCheck = db.callProcedure('getIpAddressCheck', (ipAddress,))
        print(f"Indirizzo {ipAddressCheck}")
        if len(ipAddressCheck) > 0:
            if all(key in data for key in ['id_device']):
                if Functions.validateType('str', data['id_device']):
                    id_device = data['id_device']
                    resultQuery = db.callProcedure('getSensor', (id_device,))
                    return jsonify(resultQuery), 200
                else:
                    return jsonify({"message": "id_device param must be string like S1"}), 400
            else:
                resultQuery = db.callProcedure('getSensorAll', ())
                return jsonify(resultQuery), 200
        else:
            return jsonify({"message": "Ip Address not authorized"}), 401


    def post(data, ipAddress):
        return jsonify({"message": "Method not implemented"}), 501

    def put(data, ipAddress):
        return jsonify({"message": "Method not implemented"}), 501

    def delete(data, ipAddress):
        return jsonify({"message": "Method not implemented"}), 501

# Class Actuator API Routes
class ActuatorAPI:
    def get(data, ipAddress):
        ipAddressCheck = db.callProcedure('getIpAddressCheck', (ipAddress,))
        if len(ipAddressCheck) > 0:
            if all(key in data for key in ['id_device']):
                if Functions.validateType('str', data['id_device']):
                    id_device = data['id_device']
                    resultQuery = db.callProcedure('getActuator', (id_device,))
                    return jsonify(resultQuery), 200
                else:
                    return jsonify({"message": "id_device param must be string like A1"}), 400
            else:
                resultQuery = db.callProcedure('getActuatorAll', ())
                return jsonify(resultQuery), 200
        else:
            return jsonify({"message": "Ip Address not authorized"}), 401
    
    # Per gestire se ci sono piu attuatori disponibili e scegliere quello più vicino tramite le coordinate
    def getBasedOnEvent(data, ipAddress): 
        ipAddressCheck = db.callProcedure('getIpAddressCheck', (ipAddress,))
        if len(ipAddressCheck) > 0:
            if all(key in data for key in ['id_device', 'id_event']):
                if all([
                    'id_device' in data and Functions.validateType('str', data['id_device']),
                    'id_event' in data and Functions.validateType('str', data['id_event'])
                ]):
                    id_device = data['id_device']
                    id_event = data['id_event']

                    # L'indice zero per prendere solo la risposta e non il codice di risposta. Esempio di risposta completa: (<Response 173 bytes [200 OK]>, 200)
                    result = SensorAPI.get({'id_device': id_device}, ipAddress)[0].get_json()
                    
                    coordx_sensor = result[0]['coord_lat']
                    coordy_sensor = result[0]['coord_lon']

                    resultQuery = db.callProcedure('getNearestActuator', (id_event,))
                    if not resultQuery:
                        return jsonify({"message": "No actuators available"}), 404
                    else:
                        if len(resultQuery) > 1:
                            for actuator in resultQuery:
                                actuator['distance'] = abs(actuator['coord_lat'] - coordx_sensor) + abs(actuator['coord_lon'] - coordy_sensor)
                            resultQuery = sorted(resultQuery, key=lambda k: k['distance'])
                            nearest_actuator = resultQuery[0]
                            nearest_actuator.pop('distance', None)
                        else:
                            nearest_actuator = resultQuery[0]

                        nearest_actuator['coord_lat'] = coordx_sensor
                        nearest_actuator['coord_lon'] = coordy_sensor

                    return jsonify(nearest_actuator), 200
                else:
                        return jsonify({"message": "One or more parameters have not a correct type"}), 400
            else:
                return jsonify({"message": "Missing one or more parameters"}), 400
        else:
            return jsonify({"message": "Ip Address not authorized"}), 401

    def post(data, ipAddress):
        return jsonify({"message": "Method not implemented"}), 501

    def put(data, ipAddress):
        return jsonify({"message": "Method not implemented"}), 501
        
    def delete(data):
        return jsonify({"message": "Method not implemented"}), 501
    