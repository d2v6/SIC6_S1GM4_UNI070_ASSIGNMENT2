# Python Flask (Backend Server) - app.py
from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)

temp_data = None
hum_data = None

# MQTT Configuration
BROKER = "broker.emqx.io"
PORT = 8084
MQTT_WEBSOCKET = "wss://broker.emqx.io:8084/mqtt"
USERNAME = ""
PASSWORD = ""
TOPIC_TEMP = "esp32/temperature"
TOPIC_HUM = "esp32/humidity"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe([(TOPIC_TEMP, 0), (TOPIC_HUM, 0)])
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    global temp_data, hum_data
    if msg.topic == TOPIC_TEMP:
        temp_data = msg.payload.decode()
    elif msg.topic == TOPIC_HUM:
        hum_data = msg.payload.decode()
    print(f"Received {msg.topic}: {msg.payload.decode()}")

mqtt_client = mqtt.Client(client_id="", transport="websockets")
mqtt_client.on_message = on_message
if USERNAME and PASSWORD:
    mqtt_client.username_pw_set(USERNAME, PASSWORD)
mqtt_client.on_connect = on_connect
mqtt_client.tls_set()
mqtt_client.connect(BROKER, PORT, 60)
mqtt_client.subscribe([(TOPIC_TEMP, 0), (TOPIC_HUM, 0)])
mqtt_client.loop_start()

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify({"temperature": temp_data, "humidity": hum_data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
