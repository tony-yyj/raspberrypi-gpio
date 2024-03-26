from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

# 倾斜
VER= 25

GPIO.setup(VER, GPIO.OUT)
pwm = GPIO.PWM(VER, 50)
pwm.start(0)

def angleToDujtyCycle(num):
    fm = 10.0 / 180.0
    num = num * fm + 2.5
    num = int(num * 10) / 10.0
    return num

def setServoAngle(servo, angle):
    global pwm
    assert angle >= 0 and angle <= 180
    currentlyAngle = 180 - angle
    dutyCycle = angleToDujtyCycle(currentlyAngle)
    
    print(dutyCycle)
    pwm.ChangeDutyCycle(dutyCycle)
    sleep(0.3)
    pwm.ChangeDutyCycle(0)
    sleep(0.1)

def stop():
    pwm.stop()

if __name__ == "__main__":
    try:
        while(True):
            try:

                option = input('control while angle (0 ~ 180):')
                data_angle = int(option)
                if int(option) < 0: 
                    angle = 0 
                elif int(option) > 180:
                    angle = 180
                else:
                    angle = int(option)

                setServoAngle(VER, angle)
           
            except ValueError:
                print('请输入正确的数字')




    except KeyboardInterrupt:
        stop()
        GPIO.cleanup()




