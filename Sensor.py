import RPi.GPIO as GPIO
import time
import requests

# Cấu hình GPIO cho Raspberry Pi
SENSOR_1_PIN = 23
SENSOR_2_PIN = 24
SENSOR_3_PIN = 20
SENSOR_4_PIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_1_PIN, GPIO.IN)
GPIO.setup(SENSOR_2_PIN, GPIO.IN)
GPIO.setup(SENSOR_3_PIN, GPIO.IN)
GPIO.setup(SENSOR_4_PIN, GPIO.IN)
server_url = "http://desktop:5000/update_sensor"  # Thay SERVER_IP bằng địa chỉ IP của server trung tâm

raspberry_id = "pi"  # ID của Raspberry Pi này

try:
    while True:
        sensor1_state = GPIO.input(SENSOR_1_PIN)
        sensor2_state = GPIO.input(SENSOR_2_PIN)
        sensor3_state = GPIO.input(SENSOR_3_PIN)
        sensor4_state = GPIO.input(SENSOR_4_PIN)
        # Gửi dữ liệu cảm biến 1    
        data1 = {
            "raspberry_id": raspberry_id,
            "sensor_id": "sensor1ras",
            "value": sensor1_state
        }
        requests.post(server_url, json=data1)
        
        # Gửi dữ liệu cảm biến 2
        data2 = {
            "raspberry_id": raspberry_id,
            "sensor_id": "sensor2ras",
            "value": sensor2_state
        }
        requests.post(server_url, json=data2)
        data3 = {
            "raspberry_id": raspberry_id,
            "sensor_id": "sensor3ras",
            "value": sensor3_state
        }
        requests.post(server_url, json=data3)
        data4 = {
            "raspberry_id": raspberry_id,
            "sensor_id": "sensor4ras",
            "value": sensor4_state
        }
        requests.post(server_url, json=data4)
        
        time.sleep(1)
except KeyboardInterrupt:
    print("Measurement stopped by user")
    GPIO.cleanup()
    