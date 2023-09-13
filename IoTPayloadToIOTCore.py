# Import required libraries
import time 
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import random

# Define ENDPOINT, PATH_TO_CERT, PATH_TO_KEY, PATH_TO_ROOT, and TOPIC
ENDPOINT = "a1oh3a2jyy1qcf-ats.iot.us-east-1.amazonaws.com"
PATH_TO_CERT = "./certificates/certificate.pem.crt"
PATH_TO_KEY = "./certificates/private.pem.key"
PATH_TO_ROOT = "./certificates/root.pem"
TOPIC = "test/testing"

# Define the list of device names you want to use
DEVICE_NAMES = ["device1", "device2", "device3", "device4", "device5", "device6", "device7", "device8", "device9", "device10"]  # Add more names as needed

# Define the number of messages to send
RANGE = 1

# Create an MQTT client and configure it for each device
for device_name in DEVICE_NAMES:
    CLIENT_ID = device_name  # Use the device name as the client ID

    myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
    myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
    myAWSIoTMQTTClient.configureCredentials(PATH_TO_ROOT, PATH_TO_KEY, PATH_TO_CERT)

    # Connect to the AWS IoT Core MQTT broker
    myAWSIoTMQTTClient.connect()
    print(f'Begin Publish for {CLIENT_ID}')

    # Loop to send different data in each iteration
    for i in range(RANGE):
        # Create a random data payload for each device
        payload = {
            "device_id": CLIENT_ID,
            "timestamp": int(time.time()),
            "data": {
                "temperature": random.uniform(20.0, 30.0),
                "humidity": random.uniform(40.0, 70.0),
                "pressure": random.uniform(1000.0, 1020.0)
            },
            "status": "active"
        }

        # Convert the payload to a JSON string
        message_json = json.dumps(payload)

        # Publish the JSON payload to the specified topic
        myAWSIoTMQTTClient.publish(TOPIC, message_json, 1)
        print(f"Published: '{message_json}' to the topic: 'test/testing' for {CLIENT_ID}")

        # Sleep for a short duration (e.g., 1 second) between messages
        time.sleep(1)

    print(f'Publish End for {CLIENT_ID}')

    # Disconnect from the MQTT broker for each device
    myAWSIoTMQTTClient.disconnect()
