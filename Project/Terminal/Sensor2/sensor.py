import time
import random
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from classes.MQTTBroker import MQTTBroker
from classes.Functions import *
from classes.AWSConfig import *


# Device config
DEVICE_ID = 'S' + str(random.randint(10000, 99999))   
DEVICE_NAME = 'Fire Camera'
DEVICE_TYPE = 'SENSOR'
DEVICE_AREA = 'A3'
DEVICE_EVENT = 'E1'

# Civico Via, Città, Nazione
ADDRESS = "16 Via Stazione, Messina, Italia"
COORDS = Functions.getCoords(ADDRESS)
DEVICE_COORD_LAT = COORDS[0]
DEVICE_COORD_LON = COORDS[1]

# MQTT config 
mqttBroker = None 
MQTT_TOPIC_PUB = "unimesmartcity/controller" 
MQTT_TOPIC_SUB = "unimesmartcity/device" 
QoS = 0 

# Global const
SLEEP_LOOP_SEC = 1
MAX_TIMEOUT_SEC = 15
MIN_NEXT_CHECK_CONNECTION_SEC = 15

# Global vars
busy = False
deviceIsConnected = False
controllerIsConnected = False
lastStatusController = False
counterTimeout = 0
counterCheckConnection = 0
checkForConnection = True
connectionRequested = False


def checkTimeout():
    global MAX_TIMEOUT_SEC, checkForConnection, counterTimeout, controllerIsConnected, deviceIsConnected, lastStatusController, connectionRequested
    counterTimeout += 1
    if checkForConnection:
        if counterTimeout > MAX_TIMEOUT_SEC:
            controllerIsConnected = False
            lastStatusController = False
            checkForConnection = True
            connectionRequested = False
            counterTimeout = 0
            Functions.printLine("RED", ">> Device connection timeout, retrying to connect")
    else:
        if controllerIsConnected and deviceIsConnected:
            checkForConnection = False
            counterTimeout = 0


def readMessages(client, userdata, message):
    global mqttBroker, controllerIsConnected, deviceIsConnected, lastStatusController
    message = json.loads(message.payload)

    try:
        if 'message_type' in message:

            # -- If device receive an ACK from the controller
            if message['message_type'] == 'CONTROLLER_ACK':
                if message['device_id'] == DEVICE_ID:
                    controllerIsConnected = True
                    if not lastStatusController:
                        Functions.printLine("GREEN", ">> Controller is online")
                    lastStatusController = True

            # -- If device receive a confirm of connection from the controller
            if message['message_type'] == 'CONNECTION_OK':
                if message['device_id'] == DEVICE_ID:
                    deviceIsConnected = True
                    Functions.printLine("GREEN", f">> Device {DEVICE_ID} is now connected")

            # -- If device receive receive a PING from the controller then send an ACK of my presence
            if message['message_type'] == 'PING':
                if controllerIsConnected and deviceIsConnected:
                    message = {
                        'device_id': DEVICE_ID,
                        'device_type': DEVICE_TYPE
                    }
                    mqttBroker.sendMessage('PING_ACK', message)

        else:
            Functions.printLine("RED", ">> Missing 'message_type' attribute into the MQTT body message")

    except KeyError as e:
        pass


try:
    # AWS MQTT client and connection
    my_mqtt_client = AWSIoTMQTTClient(AWSConfig.client_id)
    my_mqtt_client.configureEndpoint(AWSConfig.endpoint, 8883)
    my_mqtt_client.configureCredentials(AWSConfig.root_ca, AWSConfig.private_key, AWSConfig.certificate)

    my_mqtt_client.connect()
    Functions.printLine("GREEN", ">> AWS MQTT broker connected")

    my_mqtt_client.subscribe(MQTT_TOPIC_SUB, QoS, readMessages)
    Functions.printLine("GREEN", f">> Client subscribed to {MQTT_TOPIC_SUB} topic")

    # Instance this object to use methods of class MQTTBroker to send messages
    mqttBroker = MQTTBroker(my_mqtt_client, MQTT_TOPIC_PUB, QoS)

    while True:
        if checkForConnection:
            counterCheckConnection += (SLEEP_LOOP_SEC + 1)

            # Step 1 - Check if the controller is online
            if (not controllerIsConnected and counterTimeout == 0) or (counterCheckConnection >= MIN_NEXT_CHECK_CONNECTION_SEC):
                counterCheckConnection = 0
                controllerIsConnected = False
                message = {
                    'device_id': DEVICE_ID
                }
                mqttBroker.sendMessage('CHECK_CONTROLLER', message)
            # Step 2 - Trying to join the system
            elif controllerIsConnected and not deviceIsConnected:
                if not connectionRequested:
                    message = {
                        'device_id': DEVICE_ID,
                        'device_type': DEVICE_TYPE,
                        'device_name': DEVICE_NAME,
                        'device_area': DEVICE_AREA,
                        'device_coord_lat': DEVICE_COORD_LAT,
                        'device_coord_lon': DEVICE_COORD_LON,
                        'device_event': DEVICE_EVENT
                    }
                    mqttBroker.sendMessage('CONNECTION', message)
                    connectionRequested = True
            checkForConnection = False
        else:
            # Main code - Detecting events
            if controllerIsConnected and deviceIsConnected and not busy:
                randValue = random.randint(0, 1000)
                if 970 < randValue < 1000:
                    message = {
                        'event': 'E1',
                        'device_id': DEVICE_ID
                    }
                    mqttBroker.sendMessage('EVENT', message)
                    Functions.printLine("YELLOW", f">> Event E1 detected")
            checkForConnection = True

        checkTimeout()
        time.sleep(SLEEP_LOOP_SEC)

except KeyboardInterrupt:
    my_mqtt_client.disconnect()
    Functions.printLine("RED", "\n>> AWS MQTT broker disconnected")