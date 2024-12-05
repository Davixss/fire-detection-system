# Server Flask DATABASE
# Per ricevere le richieste da parte di controller/orchestrator

from classes.Database import *
from classes.Functions import *
from flask import jsonify, request
from datetime import datetime


# Istanza del database per effettuare le query 
db = Database()


# Class Sensor API Routes
class SensorAPI:
    def get(data,ip_address):
        
        return jsonify({"message": "Method not implemented"}), 501


    def post(data,ip_address):
        ipAddressCheck = db.callProcedure('getIpAddressCheck',(ip_address,))
        if len(ipAddressCheck) > 0 : 

            if all(key in data for key in ['id_device', 'id_event', 'name', 'area', 'coord_lat', 'coord_lon']):
                if all([
                    'id_device' in data and Functions.validateType('str', data['id_device']),
                    'id_event' in data and Functions.validateType('str', data['id_event']),
                    'name' in data and Functions.validateType('str', data['name']),
                    'area' in data and Functions.validateType('str', data['area']),
                    'coord_lat' in data and Functions.validateType('float', data['coord_lat']),
                    'coord_lon' in data and Functions.validateType('float', data['coord_lon'])

                ]):
                    id_device = data['id_device']
                    id_event=data['id_event']
                    name = data['name']
                    area = data['area']
                    coord_lat = data['coord_lat']
                    coord_lon = data['coord_lon']

                    resultQuery = db.callProcedure('postSensor', (id_device, name, area, coord_lat, coord_lon, id_event,))
                    if resultQuery:  
                        return jsonify({"message": "Sensor added successfully"}), 201
                    else:
                        return jsonify({"message": "Failed to add sensor"}), 500
                else:
                    return jsonify({"message": "One or more parameters have not a correct type"}), 400
            else:
                return jsonify({"message": "Missing one or more parameters"}), 400
        else:
            return jsonify({"message": "IP Address not authorized"}), 401 

    def put(data,ip_address):
        
        ipAddressCheck = db.callProcedure('getIpAddressCheck',(ip_address,))
        if len(ipAddressCheck) > 0 :
        
            if all(key in data for key in ['id_device', 'last_alarm']):
                if all([
                    'id_device' in data and Functions.validateType('str', data['id_device']),
                    'last_alarm' in data and Functions.validateType('str', data['last_alarm'])
                ]):
                    id_device = data['id_device']
                    last_alarm = data['last_alarm']

                    resultQuery = db.callProcedure('putSensor', (id_device, last_alarm,))
                    if resultQuery:
                        return jsonify({"message": "Sensor updated successfully"}), 200
                    else:
                        return jsonify({"message": "Failed to update sensor"}), 500
                else:
                    return jsonify({"message": "One or more parameters have not a correct type"}), 400
            else:
                return jsonify({"message": "Missing one or more parameters"}), 400
        else:
            return jsonify({"message": "IP Address not authorized"}), 401 

    def delete(data,ip_address):
        ipAddressCheck = db.callProcedure('getIpAddressCheck',(ip_address,))
        if len(ipAddressCheck) > 0 :

            if all(key in data for key in ['id_device']):
                if Functions.validateType('str', data['id_device']):
                    id_device = data['id_device']
                    resultQuery = db.callProcedure('deleteSensor', (id_device,))
                    if resultQuery:
                        return jsonify({"message": "Sensor deleted successfully"}), 200
                    else:
                        return jsonify({"message": "Failed to delete sensor"}), 500
                else:
                    return jsonify({"message": "One or more parameters have not a correct type"}), 400
            else:
                return jsonify({"message": "Missing one or more parameters"}), 400
        else:
            return jsonify({"message": "IP Address not authorized"}), 401


# Class Actuator API Routes
class ActuatorAPI:
    def get(data,ip_address):
        return jsonify({"message": "Method not implemented"}), 501
    
    def post(data,ip_address):
        ipAddressCheck = db.callProcedure('getIpAddressCheck',(ip_address,))
        if len(ipAddressCheck) > 0 :
            if all(key in data for key in ['id_device', 'id_event', 'name', 'area', 'coord_lat', 'coord_lon']):
                if all([
                    'id_device' in data and Functions.validateType('str', data['id_device']),
                    'id_event' in data and Functions.validateType('str', data['id_event']),
                    'name' in data and Functions.validateType('str', data['name']),
                    'area' in data and Functions.validateType('str', data['area']),
                    'coord_lat' in data and Functions.validateType('float', data['coord_lat']),
                    'coord_lon' in data and Functions.validateType('float', data['coord_lon'])

                ]):
                    id_device = data['id_device']
                    id_event=data['id_event']
                    name = data['name']
                    area = data['area']
                    coord_lat = data['coord_lat']
                    coord_lon = data['coord_lon']

                    resultQuery = db.callProcedure('postActuator', (id_device, name, area, coord_lat, coord_lon, id_event,))
                    if resultQuery:  
                        return jsonify({"message": "Actuator added successfully"}), 201
                    else:
                        return jsonify({"message": "Failed to add actuator"}), 500
                else:
                    return jsonify({"message": "One or more parameters have not a correct type"}), 400
            else:
                return jsonify({"message": "Missing one or more parameters"}), 400
        else:
            return jsonify({"message": "IP Address not authorized"}), 401
        
            
    def put(data,ip_address):
        ipAddressCheck = db.callProcedure('getIpAddressCheck',(ip_address,))
        if len(ipAddressCheck) > 0 :
            if all(key in data for key in ['id_device', 'busy']):
                if all([
                    'id_device' in data and Functions.validateType('str', data['id_device']),
                    'busy' in data and Functions.validateType('int', data['busy'])
                ]):
                    id_device = data['id_device']
                    busy = data['busy']

                    resultQuery = db.callProcedure('putActuator', (id_device, busy,))
                    if resultQuery:
                        return jsonify({"message": "Actuator updated successfully"}), 200
                    else:
                        return jsonify({"message": "Failed to update actuator"}), 500
                else:
                    return jsonify({"message": "One or more parameters have not a correct type"}), 400
            else:
                return jsonify({"message": "Missing one or more parameters"}), 400
        else:
            return jsonify({"message": "IP Address not authorized"}), 401
        
    def delete(data,ip_address):
        ipAddressCheck = db.callProcedure('getIpAddressCheck',(ip_address,))
        if len(ipAddressCheck) > 0 :
        
            if all(key in data for key in ['id_device']):
                if Functions.validateType('str', data['id_device']):
                    id_device = data['id_device']
                    resultQuery = db.callProcedure('deleteActuator', (id_device,))
                    if resultQuery:
                        return jsonify({"message": "Actuator deleted successfully"}), 200
                    else:
                        return jsonify({"message": "Failed to delete actuator"}), 500
                else:
                    return jsonify({"message": "One or more parameters have not a correct type"}), 400
            else:
                return jsonify({"message": "Missing one or more parameters"}), 400
        else:
            return jsonify({"message": "IP Address not authorized"}), 401


# Class History Logs
class Logs:
    def get(data, ip_address):
        return jsonify({"message": "Method not implemented"}), 501
    
    def post(data, ip_address):
        ipAddressCheck = db.callProcedure('getIpAddressCheck',(ip_address,))
        if len(ipAddressCheck) > 0:
            if all(key in data for key in ['id_device', 'message_type', 'message']):
                if all([
                    'id_device' in data and Functions.validateType('str', data['id_device']),
                    'message_type' in data and Functions.validateType('str', data['message_type']),
                    'message' in data and Functions.validateType('str', data['message'])
                ]):
                    id_device = data['id_device']
                    message_type = data['message_type']
                    message = data['message']

                    now = datetime.now()
                    datetime_now = now.strftime('%Y-%m-%d %H:%M:%S')

                    resultQuery = db.callProcedure('postLog', (datetime_now, message_type, id_device, message,))
                    if resultQuery:  
                        return jsonify({"message": "System log added successfully"}), 201
                    else:
                        return jsonify({"message": "Failed to add new log"}), 500
                else:
                    return jsonify({"message": "One or more parameters have not a correct type"}), 400
            else:
                return jsonify({"message": "Missing one or more parameters"}), 400
        else:
            return jsonify({"message": "IP Address not authorized"}), 401
            
    def put(data, ip_address):
        return jsonify({"message": "Method not implemented"}), 501
        
    def delete(data, ip_address):
        return jsonify({"message": "Method not implemented"}), 501