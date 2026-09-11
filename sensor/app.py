import os
import json
import random
import time
import ssl
import paho.mqtt.client as mqtt

MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "8883"))
TOPIC = "iot/sensor/temperature"

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="Sensor_01")

# Configuration TLS Chiffr?e
client.tls_set(ca_certs="/app/certs/ca.crt", tls_version=ssl.PROTOCOL_TLS_CLIENT)
client.tls_insecure_set(True)

connected = False
while not connected:
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        connected = True
        print(" Connected to MQTT Broker over TLS!")
    except Exception as e:
        print(f"Waiting for MQTT Broker... ({e})")
        time.sleep(2)

client.loop_start()

while True:
    temp = round(random.uniform(20.0, 30.0), 1)
    payload = json.dumps({"device": "Sensor_01", "temperature": temp, "unit": "C"})
    res = client.publish(TOPIC, payload)
    print(f"Sent (TLS Encrypted): {payload}")
    time.sleep(3)
