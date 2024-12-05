# Client MQTT configuration

import random

class AWSConfig:
    client_id = "ControllerC" + str(random.randint(10000, 99999))
    endpoint = "apv9omwb522qd-ats.iot.eu-central-1.amazonaws.com"
    root_ca = "AWS-keys/AWS-RootCA-RSA.pem"
    private_key = "AWS-keys/AWS-private.pem.key"
    certificate = "AWS-keys/AWS-certificate.pem.crt"