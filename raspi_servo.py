# Raspberry Pi - servo_app.py
from flask import Flask, request
import RPi.GPIO as GPIO
import time

app_raspi = Flask(__name__)

# Khai báo chân GPIO kết nối với servo
servo_pin = 18




@app_raspi.route('/control_servo', methods=['POST'])
def control_servo():
    data = request.json

    # Trích xuất thông tin biển số
    license_plate = data.get('license_plate', '')

    # Thực hiện logic điều khiển servo dựa trên thông tin biển số
    if license_plate:
        # Khởi tạo GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servo_pin, GPIO.OUT)
        
        # Tạo đối tượng PWM với tần số 50 Hz
        pwm = GPIO.PWM(servo_pin, 50)
        # Điều khiển servo quay 90 độ trong 5 giây
        pwm.start(0)
        duty_cycle = 7.5  # Duty cycle cho góc 90 độ
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(1)

        # Điều khiển servo quay ngược lại vị trí ban đầu (0 độ) trong 5 giây
        duty_cycle = 2.5  # Duty cycle cho góc 0 độ
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(1)

        pwm.stop()

        print(f'Servo đã quay 90 độ và quay ngược lại vị trí ban đầu cho biển số: {license_plate}')

        # Trả về phản hồi cho máy chủ nếu cần
        return {'status': 'success'}
    else:
        return {'status': 'error', 'message': 'Không có thông tin biển số'}

if __name__ == '__main__':
    try:
        # Chạy ứng dụng Flask trên Raspberry Pi trên cổng 5001
        app_raspi.run(host='0.0.0.0', port=5001, debug=True)
    finally:
        # Dọn dẹp GPIO khi kết thúc chương trình
        GPIO.cleanup()

