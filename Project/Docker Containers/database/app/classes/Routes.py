# Server Flask DATABASE
# Per ricevere le richieste da parte di controller/orchestrator

from classes.Database import *
from classes.Functions import *
from flask import jsonify, request


# Istanza del database per effettuare le query 
db = Database()


# Class Sensor API Routes
class SensorAPI:
    def get(data):
        if all(key in data for key in ['id_device']):
            if Functions.validateType('str', data['id_device']):
                id_device = data['id_device']
                resultQuery = db.query(f"SELECT * FROM mapsensor WHERE id_device = '{id_device}'")
                return jsonify(resultQuery), 200
            else:
                return jsonify({"message": "id_device param must be string like S1"}), 400
        else:
            resultQuery = db.query(f"SELECT * FROM mapsensor")
            return jsonify(resultQuery), 200


    def post(data):
        if all(key in data for key in ['id_device', 'name', 'area', 'coord_x', 'coord_y']):
            if all([
                'id_device' in data and Functions.validateType('str', data['id_device']),
                'name' in data and Functions.validateType('str', data['name']),
                'area' in data and Functions.validateType('str', data['area']),
                'coord_x' in data and Functions.validateType('float', data['coord_x']),
                'coord_y' in data and Functions.validateType('float', data['coord_y'])
            ]):
                id_device = data['id_device']
                name = data['name']
                area = data['area']
                coord_x = data['coord_x']
                coord_y = data['coord_y']

                resultQuery = db.query(f"INSERT INTO mapsensor (id_device, name, area, coord_x, coord_y) VALUES ('{id_device}', '{name}', '{area}', '{coord_x}', '{coord_y}')")
                if resultQuery:  
                    return jsonify({"message": "Sensor added successfully"}), 200
                else:
                    return jsonify({"message": "Failed to add sensor"}), 500
            else:
                return jsonify({"message": "One or more parameters have not a correct type"}), 400
        else:
            return jsonify({"message": "Missing one or more parameters"}), 400

    def put(data):
        if all(key in data for key in ['id_device', 'last_alarm']):
            if all([
                'id_device' in data and Functions.validateType('str', data['id_device']),
                'last_alarm' in data and Functions.validateType('str', data['last_alarm'])
            ]):
                id_device = data['id_device']
                last_alarm = data['last_alarm']

                resultQuery = db.query(f"UPDATE mapsensor SET last_alarm = '{last_alarm}' WHERE id_device = '{id_device}'")
                if resultQuery:
                    return jsonify({"message": "Sensor updated successfully"}), 200
                else:
                    return jsonify({"message": "Failed to update sensor"}), 500
            else:
                return jsonify({"message": "One or more parameters have not a correct type"}), 400
        else:
                return jsonify({"message": "Missing one or more parameters"}), 400

    def delete(data):
        if all(key in data for key in ['id_device']):
            if Functions.validateType('str', data['id_device']):
                id_device = data['id_device']
                resultQuery = db.query(f"DELETE FROM mapsensor WHERE id_device = '{id_device}'")
                if resultQuery:
                    return jsonify({"message": "Sensor deleted successfully"}), 200
                else:
                    return jsonify({"message": "Failed to delete sensor"}), 500
            else:
                return jsonify({"message": "One or more parameters have not a correct type"}), 400
        else:
            return jsonify({"message": "Missing one or more parameters"}), 400


# Class Actuator API Routes
class ActuatorAPI:
    def get(data):
        if all(key in data for key in ['id_device']):
            if Functions.validateType('str', data['id_device']):
                id_device = data['id_device']
                resultQuery = db.query(f"SELECT * FROM mapactuator WHERE id_device = '{id_device}'")
                return jsonify(resultQuery), 200
            else:
                return jsonify({"message": "id_device param must be string like A1"}), 400
        else:
            resultQuery = db.query(f"SELECT * FROM mapactuator")
            return jsonify(resultQuery), 200
    
    # Per gestire se ci sono piu attuatori disponibili e scegliere quello più vicino tramite le coordinate
    def getBasedOnEvent(data): 
        if all(key in data for key in ['id_device', 'id_event']):
            if all([
                'id_device' in data and Functions.validateType('str', data['id_device']),
                'id_event' in data and Functions.validateType('str', data['id_event'])
            ]):
                id_device = data['id_device']
                id_event = data['id_event']

                # L'indice zero per prendere solo la risposta e non il codice di risposta. Esempio di risposta completa: (<Response 173 bytes [200 OK]>, 200)
                result = SensorAPI.get({'id_device': id_device})[0].get_json()
                
                coordx_sensor = result[0]['coord_x']
                coordy_sensor = result[0]['coord_y']

                resultQuery = db.query(f"SELECT mapactuator.* FROM `device_event` join mapactuator ON device_event.id_device = mapactuator.id_device WHERE id_event = '{id_event}' and id_device LIKE 'A%' and mapactuator.busy = '0'")
                if not resultQuery:
                    return jsonify({"message": "No actuators available"}), 404
                else:
                    if len(resultQuery) > 1:
                        for actuator in resultQuery:
                            actuator['distance'] = abs(actuator['coord_x'] - coordx_sensor) + abs(actuator['coord_y'] - coordy_sensor)
                        resultQuery = sorted(resultQuery, key=lambda k: k['distance'])
                        nearest_actuator = resultQuery[0]
                    else:
                        nearest_actuator = resultQuery[0]
                return jsonify(nearest_actuator), 200
            else:
                    return jsonify({"message": "One or more parameters have not a correct type"}), 400
        else:
            return jsonify({"message": "Missing one or more parameters"}), 400

    def post(data):
        if all(key in data for key in ['id_device', 'name', 'area', 'coord_x', 'coord_y']):
            if all([
                'id_device' in data and Functions.validateType('str', data['id_device']),
                'name' in data and Functions.validateType('str', data['name']),
                'area' in data and Functions.validateType('str', data['area']),
                'coord_x' in data and Functions.validateType('float', data['coord_x']),
                'coord_y' in data and Functions.validateType('float', data['coord_y'])
            ]):
                id_device = data['id_device']
                name = data['name']
                area = data['area']
                coord_x = data['coord_x']
                coord_y = data['coord_y']

                resultQuery = db.query(f"INSERT INTO mapactuator (id_device, name, area, coord_x, coord_y) VALUES ('{id_device}', '{name}', '{area}', '{coord_x}', '{coord_y}')")
                if resultQuery:  
                    return jsonify({"message": "Actuator added successfully"}), 200
                else:
                    return jsonify({"message": "Failed to add actuator"}), 500
            else:
                return jsonify({"message": "One or more parameters have not a correct type"}), 400
        else:
            return jsonify({"message": "Missing one or more parameters"}), 400

    def put(data):
        if all(key in data for key in ['id_device', 'busy']):
            if all([
                'id_device' in data and Functions.validateType('str', data['id_device']),
                'busy' in data and Functions.validateType('int', data['busy'])
            ]):
                id_device = data['id_device']
                busy = data['busy']

                resultQuery = db.query(f"UPDATE mapactuator SET busy = '{busy}' WHERE id_device = '{id_device}'")
                if resultQuery:
                    return jsonify({"message": "Actuator updated successfully"}), 200
                else:
                    return jsonify({"message": "Failed to update actuator"}), 500
            else:
                return jsonify({"message": "One or more parameters have not a correct type"}), 400
        else:
            return jsonify({"message": "Missing one or more parameters"}), 400
        
    def delete(data):
        return jsonify({"message": "Method not implemented"}), 501
    

# Class DeviceEventAPI API Routes
class DeviceEventAPI:
    # Gia incluso in "get based on event" api
    # def get(data):
        # id_event = data.get('id_event')
        # if id_event is None:
        #     resultQuery = db.query(f"SELECT * FROM device_event")
        # else:
        #     resultQuery = db.query(f"SELECT * FROM device_event WHERE id_event = '{id_event}'")
        # return jsonify(resultQuery), 200

    def post(data):
        if all(key in data for key in ['id_device', 'id_event']):
            if all([
                'id_device' in data and Functions.validateType('str', data['id_device']),
                'id_event' in data and Functions.validateType('str', data['id_event'])
            ]):
                id_device = data['id_device']
                id_event = data['id_event']

                resultQuery = db.query(f"INSERT INTO device_event (id_device, id_event) VALUES ('{id_device}', '{id_event}')")
                if resultQuery:  
                    return jsonify({"message": "Device event added successfully"}), 200
                else:
                    return jsonify({"message": "Failed to add device event"}), 500
            else:
                return jsonify({"message": "One or more parameters have not a correct type"}), 400
        else:
            return jsonify({"message": "Missing one or more parameters"}), 400
        
    def put(data):
        return jsonify({"message": "Method not implemented"}), 501

    def delete(data):
        return jsonify({"message": "Method not implemented"}), 501