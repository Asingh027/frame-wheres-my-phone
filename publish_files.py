import os
import time
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv

MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = os.getenv("MQTT_PORT")
MQTT_TOPIC = "local/files"

def publish_files(directory):
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                payload = file.read()
                client.publish(MQTT_TOPIC, payload)
                print(f"Published {filename}")
                time.sleep(1)  # slight delay between messages

    client.disconnect()

if __name__ == "__main__":
    publish_files("./sample_data")  # Make sure this folder exists
