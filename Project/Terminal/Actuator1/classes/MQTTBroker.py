from datetime import datetime
import json


# MQTT Config
mqttClient = None
mqttPubTopic = None
QoS = None


class MQTTBroker:
    def __init__(self, mqttClient, mqttPubTopic, QoS):
        self.mqttClient = mqttClient
        self.mqttPubTopic = mqttPubTopic
        self.QoS = QoS

    def sendMessage(self, messageType, messageParams=None):
        currentTime = datetime.now()
        formattedTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")
        message = {
            'time': formattedTime,
            'message_type': messageType
        }
        if messageParams is not None:
            message.update(messageParams)
        self.mqttClient.publish(self.mqttPubTopic, json.dumps(message), self.QoS)
        print(f"[PUB]: {message}")
