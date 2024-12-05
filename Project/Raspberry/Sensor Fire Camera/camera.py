# This code runs only into Raspberry

import time
import os
import cv2
import numpy as np
import random
import json
from picamera2 import Picamera2
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from joblib import load
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from classes.MQTTBroker import MQTTBroker
from classes.Functions import *
from classes.AWSConfig import *


# Device config
DEVICE_ID = 'S' + str(random.randint(10000, 99999))   
DEVICE_NAME = 'Fire Camera'
DEVICE_TYPE = 'SENSOR'
DEVICE_AREA = 'A2'
DEVICE_EVENT = 'E1'

# Civico Via, Città, Nazione
ADDRESS = "228 Via Cesare Battisti, Messina, Italia"
COORDS = Functions.getCoords(ADDRESS)
DEVICE_COORD_LAT = COORDS[0]
DEVICE_COORD_LON = COORDS[1]

# MQTT config 
mqttBroker = None 
MQTT_TOPIC_PUB = "unimesmartcity/controller" 
MQTT_TOPIC_SUB = "unimesmartcity/device" 
QoS = 0 

# Camera sensor config
image_name_png = "photo.png"
image_size = [2592, 1944]
min_detection_triggers = 3
system_pause_min = 2
sleep_time_normal_sec = 30

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


# Fire detectiong function
def predict_fire(image_path, model, scaler):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (150, 150))
    img = img.flatten()
    img_normalized = scaler.transform([img])
    prediction = model.predict(img_normalized)
    return prediction[0]


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


    # Trained SVM model and Scaler
    model_file = 'model/svm_model.joblib'
    svm_model = load(model_file)
    scaler_file = 'model/scaler.joblib'
    scaler = load(scaler_file)

    # Initializing camera
    picam2 = Picamera2()
    config = picam2.create_preview_configuration({"size":(image_size[0], image_size[1])})
    picam2.align_configuration(config)
    picam2.configure(config)
    picam2.start()

    # Variables
    n_detections = 0
    alarm_triggered = False
    sleep_time = sleep_time_normal_sec

    Functions.printLine("GREEN", f">> {DEVICE_ID} {DEVICE_NAME} Pi Camera ready")
    


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
                # Shot a photo and save the .png
                picam2.capture_file(image_name_png)
                prediction = predict_fire(image_name_png, svm_model, scaler)

                if alarm_triggered == False:
                    if prediction == 1:
                        n_detections += 1
                        print(f"[FIRE {n_detections}/{min_detection_triggers}] Fire event detected!")
                        if n_detections >= min_detection_triggers:
                            print(f"[FIRE ALARM] Triggering an alert to the system")
                            print(f"[SYSTEM PAUSE] Waiting {system_pause_min}m for the next detection")
                            message = {
                                'event': 'E1',
                                'device_id': DEVICE_ID
                            }
                            mqttBroker.sendMessage('EVENT', message)
                            Functions.printLine("YELLOW", f">> Event E1 detected")
                            n_detections = 0
                            alarm_triggered = True
                            sleep_time = system_pause_min * 60
                    else:
                        print("[OK] No fire event detected")
                        n_detections = 0
                else:
                    alarm_triggered = False
                    sleep_time = sleep_time_normal_sec

                # Remove the actual photo, allowing generating a new photo
                os.remove(image_name_png)
                time.sleep(sleep_time)

            checkForConnection = True

        checkTimeout()
        time.sleep(SLEEP_LOOP_SEC)

except KeyboardInterrupt:
    my_mqtt_client.disconnect()
    Functions.printLine("RED", "\n>> AWS MQTT broker disconnected")
