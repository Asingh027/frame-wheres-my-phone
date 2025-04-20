import json
import logging
import paho.mqtt.client as mqtt
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Environment variables (with fixes)
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))  # 🔧 Cast to int
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "test/topic")  # 🔧 Fix typo from MQTT_TOPICs

ES_HOST = os.getenv("ES_HOST")
es = Elasticsearch(ES_HOST)

# Callback for MQTT connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("✅ Connected to MQTT broker")
        client.subscribe(MQTT_TOPIC)
        logging.info(f"🔔 Subscribed to topic: {MQTT_TOPIC}")
    else:
        logging.error(f"❌ Failed to connect to MQTT broker: {rc}")

# Callback for incoming MQTT messages
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        logging.info(f"📩 Received on '{msg.topic}': {payload}")
        doc = {
            "topic": msg.topic,
            "message": json.loads(payload) if payload.strip().startswith("{") else payload
        }
        es.index(index="mqtt-data", document=doc)
        logging.info("✅ Inserted into Elasticsearch")
    except Exception as e:
        logging.error(f"❌ Failed to process message: {e}")

# Setup and connect client
client = mqtt.Client()
client.username_pw_set(os.getenv("MQTT_USER"), os.getenv("MQTT_PASS"))  # Optional
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
