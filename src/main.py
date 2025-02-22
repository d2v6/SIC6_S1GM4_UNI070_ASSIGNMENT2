from machine import Pin, I2C, SoftI2C
import sys
import time
import dht
import json
import ssd1306

# Configure LED on GPIO2
led = Pin(2, Pin.OUT)

# Configure DHT11 sensor on GPIO4
dht_sensor = dht.DHT11(Pin(4))

# Initialize I2C for OLED display
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

# Scan for I2C devices
devices = i2c.scan()
print(f"I2C devices found: {devices}")

# Initialize OLED display if found
oled = None
if devices:
    try:
        oled = ssd1306.SSD1306_I2C(128, 64, i2c)
        print("OLED initialized successfully")
    except Exception as e:
        print(f"Error initializing OLED: {e}")
else:
    print("No I2C devices found")

def update_display(temp=None, hum=None, led_status=None):
    if oled is None:
        return  # Skip if OLED isn't initialized
    try:
        oled.fill(0)  # Clear display
        oled.text("ESP32 Monitor", 0, 0)
        oled.text("-" * 10, 0, 8)
        
        if temp is not None and hum is not None:
            oled.text(f"Temp: {temp}C", 0, 20)
            oled.text(f"Hum:  {hum}%", 0, 30)
        
        if led_status is not None:
            oled.text(f"LED: {led_status}", 0, 50)
        
        oled.show()
    except Exception as e:
        print(f"Display update error: {e}")

print("ESP32 Ready")

# Update OLED initially
if oled:
    update_display(led_status="OFF")

while True:
    try:
        command = sys.stdin.readline().strip()
        print(f"DEBUG: Received command: {command}")  # Debug print
        
        if command == "led_on":
            led.value(1)
            update_display(led_status="ON")
            print(json.dumps({"type": "led", "status": "on"}))
        
        elif command == "led_off":
            led.value(0)
            update_display(led_status="OFF")
            print(json.dumps({"type": "led", "status": "off"}))

        elif command == "read_dht":
            try:
                dht_sensor.measure()
                temp = dht_sensor.temperature()
                hum = dht_sensor.humidity()
                
                update_display(temp=temp, hum=hum, led_status="ON" if led.value() else "OFF")
                
                data = {
                    "type": "sensor",
                    "temperature": temp,
                    "humidity": hum
                }
                print(json.dumps(data))
            except Exception as sensor_error:
                error_msg = {"type": "error", "message": str(sensor_error)}
                print(json.dumps(error_msg))

        time.sleep(0.1)
    
    except Exception as e:
        error_msg = {"type": "error", "message": str(e)}
        print(json.dumps(error_msg))
        time.sleep(1)
