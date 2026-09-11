import os
import json
import time
import ssl
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "8883"))
TOPIC = "iot/sensor/temperature"

INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG", "iot_org")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "temperature_data")

influx_client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = influx_client.write_api(write_options=SYNCHRONOUS)

def on_connect(client, userdata, flags, reason_code, properties):
    print("Bridge connected to MQTT over TLS!")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        point = Point("temperature").tag("device", data["device"]).field("value", float(data["temperature"]))
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        print(f"Stored in InfluxDB: {data}")
    except Exception as e:
        print(f"Error: {e}")

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="influx_bridge")
client.on_connect = on_connect
client.on_message = on_message

client.tls_set(ca_certs="/app/certs/ca.crt", tls_version=ssl.PROTOCOL_TLS_CLIENT)
client.tls_insecure_set(True)

connected = False
while not connected:
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        connected = True
    except Exception as e:
        print(f"Bridge waiting for MQTT... ({e})")
        time.sleep(2)

client.loop_forever()
