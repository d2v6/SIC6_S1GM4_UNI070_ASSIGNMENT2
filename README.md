# SIC6_S1GM4_UNI070_ASSIGNMENT2

## Overview
This project integrates an ESP32 microcontroller with a Python Flask backend to collect temperature and humidity data using a **DHT11 sensor**. The data is then **published via MQTT**, stored in a **MongoDB database**, and sent to **Ubidots** for cloud monitoring.

## System Architecture
- **ESP32** with DHT11 sensor for data collection
- **MQTT** for data transmission
- **MongoDB** for local data storage
- **Flask** backend server
- **Ubidots** for cloud visualization

## Prerequisites
- Python 3.8+
- ESP32 board
- DHT11 sensor
- USB cable
- MongoDB installed locally
- Ubidots account

## Installation Steps

### 1. Install Required Python Packages
```bash
pip install esptool
pip install adafruit-ampy
pip install pyserial
pip install flask
pip install paho-mqtt
pip install pymongo
pip install requests
```

### 2. Flash ESP32 with MicroPython
1. Download MicroPython firmware for ESP32 from [official website](https://micropython.org/download/esp32/)
2. Erase ESP32 flash memory:
```bash
python -m esptool --port COM3 erase_flash
```
3. Flash MicroPython firmware:
```bash
python -m esptool --port COM3 --baud 460800 write_flash --flash_size=detect 0x1000 firmware.bin
```

### 3. Upload Required Files to ESP32
1. Upload MQTT helper library:
```bash
ampy --port COM3 put simple.py
```
2. Upload main program:
```bash
ampy --port COM3 put main.py
```

### 4. Configure the Project

#### ESP32 Configuration (main.py)
1. Update WiFi credentials:
```python
SSID = "your_wifi_ssid"
PASSWORD = "your_wifi_password"
```

#### Flask Server Configuration (app.py)
1. Update MongoDB settings if needed:
```python
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "S1GM4"
COLLECTION_NAME = "sensor_data"
```

2. Update Ubidots configuration:
```python
UBIDOTS_TOKEN = "YOUR-UBIDOTS-TOKEN"
UBIDOTS_DEVICE_LABEL = "esp32"
```

### 5. Start the System

1. Start MongoDB service (if not running):
```bash
mongod --dbpath <your-db-path>
```

2. Monitor ESP32 output (in terminal 1):
```bash
python -m serial.tools.miniterm COM3 115200
```

3. Start Flask server (in terminal 2):
```bash
python app.py
```

### 6. Verify Operation

1. **Check ESP32 Connection**
   - ESP32 should connect to WiFi
   - You should see MQTT messages being published

2. **Verify MongoDB Storage**
   - Use MongoDB Compass to check if data is being stored
   - Database: S1GM4
   - Collection: sensor_data

3. **Check Ubidots Dashboard**
   - Log into Ubidots
   - Go to Devices > esp32
   - Verify data is being received

4. **Test Flask API**
```bash
curl http://localhost:5000/data
```

### Troubleshooting

1. **ESP32 Connection Issues**
   - Verify correct COM port
   - Check USB cable
   - Try pressing ESP32 reset button

2. **MQTT Problems**
   - Verify WiFi connection
   - Check MQTT broker status
   - Verify topic names

3. **MongoDB Issues**
   - Ensure MongoDB service is running
   - Check connection string
   - Verify database permissions

4. **Ubidots Connection**
   - Verify token is correct
   - Check internet connection
   - Verify device label matches

## Project Structure
```
project/
├── src/
│   ├── main.py      # ESP32 code
│   ├── simple.py    # MQTT helper
│   └── app.py       # Flask server
└── README.md
```

## Common Commands

### ESP32 Management
```bash
# List COM ports
python -m serial.tools.list_ports

# Monitor ESP32
python -m serial.tools.miniterm COM3 115200

# Reset ESP32
ampy --port COM3 reset
```

### Data Verification
```bash
# Get latest readings
curl http://localhost:5000/data

# MongoDB query (in MongoDB shell)
use S1GM4
db.sensor_data.find().sort({timestamp:-1}).limit(1)
```

## Contributors
- **Dave Daniell Yanni**
- **Alvin Christopher Santausa**
- **Michael Ballard Isaiah Silaen**
- **Kenneth Poenadi**

---
