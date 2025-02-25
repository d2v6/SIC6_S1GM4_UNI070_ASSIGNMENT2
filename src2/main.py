# MicroPython (ESP32) - main.py
import network
import time
import dht
import machine
from umqtt.simple import MQTTClient

# WiFi Credentials
SSID = "nicequota"
PASSWORD = "mywifi123"

# MQTT Broker (Flask server IP or cloud broker)
BROKER = "broker.emqx.io"  # Public MQTT broker
TOPIC_TEMP = b"esp32/temperature"
TOPIC_HUM = b"esp32/humidity"

# DHT Sensor Configuration
dht_pin = machine.Pin(4)
dht_sensor = dht.DHT11(dht_pin)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print("WiFi Scan:", wlan.scan())

    wlan.connect("nicequota", PASSWORD)

    print("Connecting to WiFi...")

    timeout = 10
    start = time.time()

    while not wlan.isconnected():
        if time.time() - start > timeout:
            print("WiFi Connection Timeout! Restarting ESP32...")
            machine.reset()
        time.sleep(1)
        print(".", end="")

    print("\nWiFi Connected:", wlan.ifconfig())


# Connect to MQTT broker
def connect_mqtt():
    print("🔄 Connecting to MQTT broker...")
    try:
        client = MQTTClient("esp32", BROKER)
        client.connect()
        print("Connected to MQTT broker")
        return client
    except Exception as e:
        print("MQTT Connection Failed:", e)
        return None

# Start WiFi and MQTT
connect_wifi()
mqtt_client = connect_mqtt()

while True:
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()
        
        print(f"Sending Data -> Temperature: {temp}C, Humidity: {hum}%")
        
        if mqtt_client:
            mqtt_client.publish(TOPIC_TEMP, str(temp))
            mqtt_client.publish(TOPIC_HUM, str(hum))
            print("Data Sent to MQTT")
        else:
            print("MQTT Client Not Connected")
        
    except Exception as e:
        print("Error reading sensor:", e)
    
    time.sleep(5)
