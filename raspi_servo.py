from flask import Flask, request
import RPi.GPIO as GPIO
import time
import liquidcrystal_i2c

app_raspi = Flask(__name__)
# Khai báo chân GPIO kết nối với servo
servo_pin_open = 24  # Chân GPIO cho servo mở
servo_pin_close = 18  # Chân GPIO cho servo đóng
# Khởi tạo GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin_open, GPIO.OUT)
GPIO.setup(servo_pin_close, GPIO.OUT)
# Tạo đối tượng PWM cho servo mở và servo đóng với tần số 50 Hz
pwm_open = GPIO.PWM(servo_pin_open, 50)
pwm_open.start(0)
pwm_close = GPIO.PWM(servo_pin_close, 50)
pwm_close.start(0)
rows = 4
lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x26, 1, numlines=rows)
lcd.printline(0, 'Xin Chao  ACTVN')

def set_angle_open(angle):
    duty_cycle = (angle / 18) + 2
    GPIO.output(servo_pin_open, True)
    pwm_open.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    GPIO.output(servo_pin_open, False)
    pwm_open.ChangeDutyCycle(0)

def set_angle_close(angle):
    duty_cycle = (angle / 18) + 2
    GPIO.output(servo_pin_close, True)
    pwm_close.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    GPIO.output(servo_pin_close, False)
    pwm_close.ChangeDutyCycle(0)

def return_to_initial_position():
    set_angle_open(0)  # Quay servo mở về vị trí ban đầu
    set_angle_close(0)  # Quay servo đóng về vị trí ban đầu

@app_raspi.route('/open', methods=['POST'])
def open_servo():
    # Điều khiển servo mở
    set_angle_open(90)  # Điều chỉnh góc mở tùy thuộc vào servo
    time.sleep(5)  # Chờ 5 phút
    set_angle_open(0)    # Quay trở lại vị trí ban đầu
    return {'status': 'success'}

@app_raspi.route('/close', methods=['POST'])
def close_servo():
    # Điều khiển servo đóng
    set_angle_close(90)  # Điều chỉnh góc đóng tùy thuộc vào servo
    time.sleep(5)  # Chờ 5 phút
    set_angle_close(0)  # Quay trở lại vị trí ban đầu
    return {'status': 'success'}

@app_raspi.route('/receive_text', methods=['POST'])
def receive_filtered_string():
    data = request.json
    filtered_string = data.get('filtered_string')

    if filtered_string:
        # Xử lý filtered_string ở đây
        print("Filtered string received:", filtered_string)
        lcd.printline(0, '                             ')
        lcd.printline(1, '                             ')
        lcd.printline(0, 'Bien So Xe: ')

        lcd.printline(1, filtered_string)
        return {'status': 'success'}
    else:
        return {'status': 'error', 'message': 'Không có dữ liệu filtered_string'}

if __name__ == '__main__':
    try:
        # Chạy ứng dụng Flask trên Raspberry Pi trên cổng 5001
        app_raspi.run(host='0.0.0.0', port=5001, debug=True)
    finally:
        # Dọn dẹp GPIO khi kết thúc chương trình
        pwm_open.stop()
        pwm_close.stop()
        GPIO.cleanup()
