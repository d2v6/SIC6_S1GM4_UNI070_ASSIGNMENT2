from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt
import pymongo
import requests
import json
from datetime import datetime

app = Flask(__name__)

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017/"  # Change accordingly
DB_NAME = "S1GM4" # Change accordingly
COLLECTION_NAME = "sensor_data" # Change accordingly

# Connect to MongoDB
mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db[COLLECTION_NAME]

# MQTT Configuration
BROKER = "broker.emqx.io"
PORT = 8084
MQTT_WEBSOCKET = "wss://broker.emqx.io:8084/mqtt"
USERNAME = ""
PASSWORD = ""
TOPIC_TEMP = "esp32/temperature"
TOPIC_HUM = "esp32/humidity"

# Ubidots Configuration
UBIDOTS_TOKEN = "BBUS-AaVanj19JGa3mHFr0BpMU8VXC4XX1v"  # Replace with your Ubidots TOKEN
UBIDOTS_DEVICE_LABEL = "esp32"  # Device label in Ubidots
UBIDOTS_API_URL = f"https://industrial.api.ubidots.com/api/v1.6/devices/{UBIDOTS_DEVICE_LABEL}"

def send_to_ubidots(temperature, humidity):
    """Send sensor data to Ubidots"""
    try:
        headers = {
            "X-Auth-Token": UBIDOTS_TOKEN,
            "Content-Type": "application/json"
        }
        
        payload = {
            "temperature": float(temperature),
            "humidity": float(humidity)
        }
        
        response = requests.post(
            UBIDOTS_API_URL, 
            headers=headers,
            data=json.dumps(payload)
        )
        
        if response.status_code == 200:
            print("Data sent to Ubidots successfully")
        else:
            print(f"Failed to send data to Ubidots: {response.status_code}")
            
    except Exception as e:
        print(f"Error sending data to Ubidots: {e}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe([(TOPIC_TEMP, 0), (TOPIC_HUM, 0)])
    else:
        print(f" Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    """Handles incoming MQTT messages, saves to MongoDB, and sends to Ubidots"""
    try:
        value = float(msg.payload.decode())  # Convert to float
        data = {
            "timestamp": datetime.utcnow(),
            "topic": msg.topic,
            "value": value
        }
        collection.insert_one(data)  # Store in MongoDB
        print(f"sStored in MongoDB: {data}")

        # Retrieve latest values
        latest_temp = collection.find_one({"topic": TOPIC_TEMP}, sort=[("timestamp", -1)])
        latest_hum = collection.find_one({"topic": TOPIC_HUM}, sort=[("timestamp", -1)])

        if latest_temp and latest_hum:
            send_to_ubidots(latest_temp["value"], latest_hum["value"])

    except Exception as e:
        print(f"Error processing MQTT message: {e}")

# Setup MQTT Client
mqtt_client = mqtt.Client(client_id="", transport="websockets")
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
if USERNAME and PASSWORD:
    mqtt_client.username_pw_set(USERNAME, PASSWORD)
mqtt_client.tls_set()
mqtt_client.connect(BROKER, PORT, 60)
mqtt_client.loop_start()

@app.route("/data", methods=["GET"])
def get_data():
    """Retrieve the latest temperature and humidity from MongoDB"""
    latest_temp = collection.find_one({"topic": TOPIC_TEMP}, sort=[("timestamp", -1)])
    latest_hum = collection.find_one({"topic": TOPIC_HUM}, sort=[("timestamp", -1)])

    return jsonify({
        "temperature": latest_temp["value"] if latest_temp else None,
        "humidity": latest_hum["value"] if latest_hum else None
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
