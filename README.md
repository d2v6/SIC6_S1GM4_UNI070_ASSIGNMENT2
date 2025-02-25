# SIC6_S1GM4_UNI070_ASSIGNMENT2

## Overview
This project integrates an ESP32 microcontroller with a Python Flask backend to collect temperature and humidity data using a **DHT11 sensor**. The data is then **published via MQTT**, stored in a **MongoDB database**, and sent to **Ubidots** for cloud monitoring.

## Features
- ESP32 reads **temperature & humidity** using DHT11 sensor
- Sends data to **Flask server** via **MQTT**
- Stores data in a **MongoDB local database**
- Sends data to **Ubidots cloud platform**
- Flask **API endpoint** to retrieve latest data

---

## Hardware Requirements
- **ESP32 Board**
- **DHT11 Temperature & Humidity Sensor**
- **Jumper Wires**
- **WiFi Connection**

## Software Requirements
- **Python 3.8+**
- **Flask** (Backend Server)
- **paho-mqtt** (MQTT client for Python)
- **MongoDB** (Local database)
- **Ubidots API Key** (For cloud storage)
- **MicroPython** installed on ESP32
- **MQTT Broker** (EMQX or a self-hosted broker)

---

## Project Setup

### 1️⃣ Flash MicroPython on ESP32
Ensure **MicroPython** is installed on your ESP32 board.

1. Install **esptool**:
   ```sh
   pip install esptool
   ```
2. Erase ESP32 flash:
   ```sh
   esptool.py --chip esp32 erase_flash
   ```
3. Flash MicroPython firmware:
   ```sh
   esptool.py --chip esp32 --port COMx write_flash -z 0x1000 firmware.bin
   ```
   _(Replace `COMx` with your port and `firmware.bin` with the actual MicroPython firmware file)_

### 2️⃣ Upload `main.py` to ESP32
Use **Thonny** or **ampy** to upload `main.py` to ESP32.

```sh
ampy --port COMx put main.py
```

### 3️⃣ Run Flask Backend (`app.py`)
Make sure **MongoDB is running** and Flask dependencies are installed.

#### Install Dependencies
```sh
pip install flask paho-mqtt pymongo requests
```

#### Start MongoDB (if not running)
```sh
mongod --dbpath <your-db-path>
```

#### Run Flask Server
```sh
python app.py
```
Flask server will start at `http://0.0.0.0:5000`

### 4️⃣ Setup MQTT Broker
- The ESP32 **publishes** data to MQTT broker (`broker.emqx.io`)
- Flask **subscribes** to MQTT topics: `esp32/temperature` & `esp32/humidity`

### 5️⃣ Ubidots Configuration
- Replace `UBIDOTS_TOKEN` in `app.py` with your Ubidots **API Key**
- Data is sent to Ubidots automatically when received from ESP32

---

## Usage Guide

### **1️⃣ Run ESP32 Code**
ESP32 will:
- Connect to **WiFi**
- Read **DHT11** sensor data
- Send data via **MQTT**

### **2️⃣ Check Flask Server Logs**
Flask will:
- Subscribe to **MQTT topics**
- Save received data to **MongoDB**
- Send data to **Ubidots**

### **3️⃣ Access Data via API**
To get the latest stored data:
```sh
curl http://localhost:5000/data
```
Example Response:
```json
{
  "temperature": 25.4,
  "humidity": 60.3
}
```

### **4️⃣ Monitor Data in Ubidots**
Log into **Ubidots** and check the **ESP32 device dashboard** for real-time sensor data.

---

## Troubleshooting
### ❌ ESP32 Not Connecting to WiFi
- Double-check **SSID & Password** in `main.py`
- Restart ESP32 and try again

### ❌ MQTT Not Connecting
- Ensure MQTT broker (`broker.emqx.io`) is online
- Check if Flask can connect to the broker

### ❌ Data Not Appearing in MongoDB
- Ensure MongoDB service is **running**
- Check Flask logs for errors

### ❌ Data Not Showing in Ubidots
- Verify **API Key** in `app.py`
- Check **Ubidots Device Label**

---

## Future Improvements
✅ Implement **JWT Authentication** for Flask API
✅ Use **WebSocket Dashboard** for real-time visualization
✅ Deploy **Flask App on DigitalOcean** for remote access

---

## Contributors
- **Dave Daniell Yanni**
- **Alvin Christopher Santausa**
- **Michael Ballard Isaiah Silaen**
- **Kenneth Poenadi**

---

## License
This project is open-source under the MIT License. Feel free to modify and improve!

