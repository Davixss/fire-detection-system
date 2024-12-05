import time
import asyncio
import json

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from classes.Functions import *
from classes.AWSConfig import *
from classes.MQTTBroker import MQTTBroker
from classes.FlaskClient import *
from classes.FlaskConfig import *
import copy
from datetime import datetime, timedelta


# Device config
CONTROLLER_ID = 'C1'
CONTROLLER_NAME = 'Device Controller'

# MQTT config
mqttBroker = None
MQTT_TOPIC_PUB = "unimesmartcity/device"
MQTT_TOPIC_SUB = "unimesmartcity/controller"
QoS = 0

# Global consts
SEND_PING_TIME_SEC = 30

# Memory of devices
DevicesList = {
    'SENSOR': [],
    'ACTUATOR': []
}


def addDevice(device_type, device_id):
    global DevicesList
    if device_id not in DevicesList[device_type]:
        DevicesList[device_type].append(device_id)


def readMessages(client, userdata, message):
    global DevicesList, mqttBroker
    message = json.loads(message.payload)

    if 'message_type' in message:
        # -- Device ask to verify if controller is online
        if message['message_type'] == 'CHECK_CONTROLLER':
            json_message = {
                'device_id': message['device_id']
            }
            mqttBroker.sendMessage('CONTROLLER_ACK', json_message)

        # -- Device login
        if message['message_type'] == 'CONNECTION':
            device_id = message['device_id']
            device_type = message['device_type']
            device_name = message['device_name']
            device_area = message['device_area']
            device_coord_lat = message['device_coord_lat']
            device_coord_lon = message['device_coord_lon']
            device_event = message['device_event']

            data = {
                'id_device': device_id
            }

            

            if device_type == 'SENSOR' :
                response = FlaskClient.sendRequest(ServerProxy.FLASK_HOST, ServerProxy.FLASK_PORT, 'GET', '/orchestrator/sensor', data)
                if len(response) == 0:
                    data = {
                        'id_device': device_id,
                        'name': device_name,
                        'area': device_area,
                        'coord_lat': device_coord_lat,
                        'coord_lon': device_coord_lon,
                        'id_event': device_event
                    }
                    FlaskClient.sendRequest(ServerProxy.FLASK_HOST, ServerProxy.FLASK_PORT, 'POST', '/controller/sensor', data)
            else :
                response = FlaskClient.sendRequest(ServerProxy.FLASK_HOST, ServerProxy.FLASK_PORT, 'GET', '/orchestrator/actuator', data)
                if len(response) == 0:
                    data = {
                        'id_device': device_id,
                        'name': device_name,
                        'area': device_area,
                        'coord_lat': device_coord_lat,
                        'coord_lon': device_coord_lon,
                        'id_event': device_event
                    }
                    FlaskClient.sendRequest(ServerProxy.FLASK_HOST, ServerProxy.FLASK_PORT, 'POST', '/controller/actuator', data)
                
            json_message = {
                'device_id': message['device_id']
            }
            mqttBroker.sendMessage('CONNECTION_OK', json_message)
            addDevice(device_type, device_id)
            
        # -- ACK received
        if message['message_type'] == 'PING_ACK':
            device_id = message['device_id']
            device_type = message['device_type']
            addDevice(device_type, device_id)

        # -- Event triggered
        if message['message_type'] == 'EVENT':
            event = message['event']
            device_id = message['device_id']

            Functions.printLine("YELLOW", f">> Event {event} triggered from the device {device_id}")
            currentTime = datetime.now() + timedelta(hours=1)
            formattedTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
            data = {
                    'id_device': device_id,
                    'id_event': event,
                    'last_alarm': formattedTime
                    }
            FlaskClient.sendRequest(ServerProxy.FLASK_HOST, ServerProxy.FLASK_PORT, 'PUT', '/controller/sensor', data)
            
            # Add log into database
            json_message = {
                'id_device': device_id,
                'message_type': 'EVENT',
                'message': f'Event {event} triggered from the device {device_id}'
            }
            FlaskClient.sendRequest(ServerProxy.FLASK_HOST, ServerProxy.FLASK_PORT, 'POST', '/controller/log', json_message)
            
            actuator = FlaskClient.sendRequest(ServerProxy.FLASK_HOST, ServerProxy.FLASK_PORT, 'GET', '/orchestrator/actuator_based_on_event', data)
            
            if actuator is not None:
                json_message = {
                    'id_device': actuator['id_device'],
                    'coord_lat': actuator['coord_lat'],
                    'coord_lon': actuator['coord_lon'],
                    'busy' : '1'
                }
                mqttBroker.sendMessage('ACTUATOR_ACTIVATED', json_message)
                FlaskClient.sendRequest(ServerProxy.FLASK_HOST, ServerProxy.FLASK_PORT, 'PUT', '/controller/actuator', json_message)

                # Add log into database
                json_message = {
                    'id_device': actuator['id_device'],
                    'message_type': 'ACTUATOR_ACTIVATED',
                    'message': f"Event {event} triggered from the device {device_id} | Lat: {actuator['coord_lat']}, Lon: {actuator['coord_lon']}"
                }
                FlaskClient.sendRequest(ServerProxy.FLASK_HOST, ServerProxy.FLASK_PORT, 'POST', '/controller/log', json_message)


            else:
                Functions.printLine("YELLOW", ">> No actuator available")
     
                
    else:
        Functions.printLine("RED", ">> Missing 'message_type' attribute into the MQTT body message")

        


async def sendPingToDevices():
    global mqttBroker, DevicesList
    await asyncio.sleep(10)
    tmp_DeviceList = None
    
    while True:
        # Clearing actual devices list
        tmp_DeviceList = copy.deepcopy(DevicesList)
        DevicesList['SENSOR'].clear()
        DevicesList['ACTUATOR'].clear()
        mqttBroker.sendMessage('PING')
        await asyncio.sleep(SEND_PING_TIME_SEC)

        # tmp_DeviceList['SENSOR'] = [1, 7, 9, 4]
        # DeviceList['SENSOR'] = [1, 7, 4]

        for device in tmp_DeviceList['SENSOR']:
            if device not in DevicesList['SENSOR']:
                json_message = {
                    'id_device': device
                }
                FlaskClient.sendRequest(ServerProxy.FLASK_HOST, ServerProxy.FLASK_PORT, 'DELETE', '/controller/sensor', json_message)
                Functions.printLine("RED", f">> Sensor {device} left the system")
                json_message = {
                    'id_device': device,
                    'message_type': 'EVENT',
                    'message': f'Sensor {device} left the system'
                }
                FlaskClient.sendRequest(ServerProxy.FLASK_HOST, ServerProxy.FLASK_PORT, 'POST', '/controller/log', json_message)

        for device in tmp_DeviceList['ACTUATOR']:
            if device not in DevicesList['ACTUATOR']:
                json_message = {
                    'id_device': device
                }
                FlaskClient.sendRequest(ServerProxy.FLASK_HOST, ServerProxy.FLASK_PORT, 'DELETE', '/controller/actuator', json_message)
                Functions.printLine("RED", f">> Actuator {device} left the system")
                json_message = {
                    'id_device': device,
                    'message_type': 'EVENT',
                    'message': f'Actuator {device} left the system'
                }
                FlaskClient.sendRequest(ServerProxy.FLASK_HOST, ServerProxy.FLASK_PORT, 'POST', '/controller/log', json_message)

        



try:
    # Create a MQTT client
    my_mqtt_client = AWSIoTMQTTClient(AWSConfig.client_id)
    my_mqtt_client.configureEndpoint(AWSConfig.endpoint, 8883)
    my_mqtt_client.configureCredentials(AWSConfig.root_ca, AWSConfig.private_key, AWSConfig.certificate)

    # Broker connection
    my_mqtt_client.connect()
    Functions.printLine("GREEN", ">> MQTT broker connected")

    # Topic subscription
    my_mqtt_client.subscribe(MQTT_TOPIC_SUB, QoS, readMessages)
    Functions.printLine("GREEN", f">> Client subscribed to {MQTT_TOPIC_SUB} topic")

    # Connect to AWS broker
    mqttBroker = MQTTBroker(my_mqtt_client, MQTT_TOPIC_PUB, QoS)

    asyncio.run(sendPingToDevices())

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    my_mqtt_client.disconnect()
    Functions.printLine("RED", "\n>> AWS MQTT broker disconnected")
