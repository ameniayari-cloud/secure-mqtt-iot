import json
import os
import ssl
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point

MQTT_BROKER = os.getenv("MQTT_BROKER", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "8883"))
MQTT_TOPIC = "iot/sensor/temperature"

INFLUX_URL = os.getenv("INFLUX_URL", "http://influxdb:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG", "iot_org")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "temperature_data")

influx_client = InfluxDBClient(
    url=INFLUX_URL,
    token=INFLUX_TOKEN,
    org=INFLUX_ORG
)

write_api = influx_client.write_api()

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to MQTT: {reason_code}", flush=True)
    client.subscribe(MQTT_TOPIC)
    print(f"Subscribed to: {MQTT_TOPIC}", flush=True)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())

        point = (
            Point("temperature")
            .tag("device", data["device"])
            .field("value", float(data["temperature"]))
            .field("unit", data.get("unit", "C"))
        )

        write_api.write(
            bucket=INFLUX_BUCKET,
            org=INFLUX_ORG,
            record=point
        )

        print(f"Stored in InfluxDB: {data}", flush=True)

    except Exception as error:
        print(f"Error: {error}", flush=True)

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="influx_bridge"
)

client.tls_set(
    ca_certs="/app/certs/ca.crt",
    certfile="/app/certs/client.crt",
    keyfile="/app/certs/client.key",
    tls_version=ssl.PROTOCOL_TLS_CLIENT
)

client.on_connect = on_connect
client.on_message = on_message

print("Starting MQTT to InfluxDB bridge...", flush=True)

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()