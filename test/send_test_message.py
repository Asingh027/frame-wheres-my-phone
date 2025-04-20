import paho.mqtt.publish as publish
import json
import time
from datetime import datetime

while True:
    payload = {
        "device": "test",
        "value": 42,
        "status": "active",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    publish.single(
        topic="test/topic",
        payload=json.dumps(payload),
        hostname="localhost",
        port=1883
    )

    print(f"Published at {payload['timestamp']}")
    time.sleep(2)
