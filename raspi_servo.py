from flask import Flask
from flask import request
import RPi.GPIO as GPIO
import time

app_raspi = Flask(__name__)

# Khai báo chân GPIO kết nối với servo
servo_pin = 18

# Khởi tạo GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Tạo đối tượng PWM với tần số 50 Hz
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

@app_raspi.route('/open', methods=['POST'])
def open_servo():
    # Điều khiển servo mở
    duty_cycle = 7.5  # Duty cycle cho góc mở
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep()
    duty_cycle = 2.5  # Duty cycle cho góc đóng
    pwm.ChangeDutyCycle(duty_cycle)

    return {'status': 'success'}

@app_raspi.route('/close', methods=['POST'])
def close_servo():
    # Điều khiển servo đóng
    duty_cycle = 2.5  # Duty cycle cho góc đóng
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    return {'status': 'success'}

if __name__ == '__main__':
    try:
        # Chạy ứng dụng Flask trên Raspberry Pi trên cổng 5001
        app_raspi.run(host='0.0.0.0', port=5001, debug=True)
    finally:
        # Dọn dẹp GPIO khi kết thúc chương trình
        pwm.stop()
        GPIO.cleanup()
