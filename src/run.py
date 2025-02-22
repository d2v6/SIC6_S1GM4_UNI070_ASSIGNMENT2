# PC Code (run.py)
import serial
import time
import json
from datetime import datetime

ESP32_PORT = "COM3"  # Change to your port
BAUD_RATE = 115200

def read_esp_response(esp, timeout=2):
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        if esp.in_waiting:
            try:
                line = esp.readline().decode('utf-8').strip()
                if line:
                    return json.loads(line)
            except (json.JSONDecodeError, UnicodeDecodeError):
                continue
    return None

def format_sensor_data(data):
    current_time = datetime.now().strftime("%H:%M:%S")
    temp = data.get("temperature")
    hum = data.get("humidity")
    return f"[{current_time}] Temperature: {temp}°C, Humidity: {hum}%"

try:
    esp = serial.Serial(ESP32_PORT, BAUD_RATE, timeout=1)
    print("Connecting to ESP32...")
    time.sleep(2)
    
    # Clear initial boot messages
    esp.reset_input_buffer()

    print("\nESP32 Serial Monitor")
    print("Commands: 'on' (LED on), 'off' (LED off), 'read' (DHT sensor), 'exit'")

    while True:
        command = input("\nEnter command: ").strip().lower()

        if command == "exit":
            print("Exiting...")
            break

        if command in ["on", "off", "read"]:
            esp.reset_input_buffer()
            
            if command == "on":
                esp.write(b'led_on\n')
            elif command == "off":
                esp.write(b'led_off\n')
            elif command == "read":
                esp.write(b'read_dht\n')
            
            time.sleep(0.5)
            response = read_esp_response(esp)
            
            if response:
                if response["type"] == "led":
                    print(f"LED is now {response['status'].upper()}")
                elif response["type"] == "sensor":
                    print(format_sensor_data(response))
                elif response["type"] == "error":
                    print(f"Error: {response['message']}")
            else:
                print("No response received")
        else:
            print("Invalid command. Use 'on', 'off', 'read', or 'exit'.")

except serial.SerialException as e:
    print(f"Serial Error: {e}")
    print("Please check if the correct port is selected and the ESP32 is connected.")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'esp' in locals():
        esp.close()