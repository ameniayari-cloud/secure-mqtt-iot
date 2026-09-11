import json
import os
import random
import ssl
import time
import paho.mqtt.client as mqtt

MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "8883"))
MQTT_TOPIC = "iot/sensor/temperature"
DEVICE_ID = "Sensor_01"

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to MQTT: {reason_code}")

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id=DEVICE_ID
)

client.tls_set(
    ca_certs="/app/certs/ca.crt",
    certfile="/app/certs/client.crt",
    keyfile="/app/certs/client.key",
    tls_version=ssl.PROTOCOL_TLS_CLIENT
)

client.on_connect = on_connect
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

while True:
    temperature = round(random.uniform(20.0, 30.0), 1)

    payload = json.dumps({
        "device": DEVICE_ID,
        "temperature": temperature,
        "unit": "C"
    })

    result = client.publish(MQTT_TOPIC, payload)
    print(f"Published: {payload} | Status: {result.rc}")
    time.sleep(2)
