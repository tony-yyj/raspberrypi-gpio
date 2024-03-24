import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)


# --- TB6612FNG ----
STBY = 27
PWMA = 18
AIN1 = 14
AIN2 = 15
PWMB = 19
BIN1 = 23
BIN2 = 24

GPIO.setup(STBY, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)

GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

pwma = GPIO.PWM(PWMA, 300)
pwmb = GPIO.PWM(PWMB, 300)
# ----------------

# --- SG90s ---

# vertical axis Y
VER = 25
# horizontal axis X
HOR = 17

GPIO.setup(VER, GPIO.OUT)
GPIO.setup(HOR, GPIO.OUT)
# ----------------





# 前进或后退（大于0前进，小于0后退）
def goForward(speed):
    if (speed >= 0):
        GPIO.output(AIN1, GPIO.LOW)
        GPIO.output(AIN2, GPIO.HIGH)
        GPIO.output(BIN1, GPIO.LOW)
        GPIO.output(BIN2, GPIO.HIGH)
        pwma.start(speed)
        pwmb.start(speed)
        sleep(0.02)
    else:
        GPIO.output(AIN1, GPIO.HIGH)
        GPIO.output(AIN2, GPIO.LOW)
        GPIO.output(BIN1, GPIO.HIGH)
        GPIO.output(BIN2, GPIO.LOW)
        pwma.start(-speed)
        pwmb.start(-speed)
        sleep(0.02)

def changeDirection(speed):
    if (speed > 0):
        GPIO.output(AIN1, GPIO.HIGH)
        GPIO.output(AIN2, GPIO.LOW)
        GPIO.output(BIN1, GPIO.LOW)
        GPIO.output(BIN2, GPIO.HIGH)
        pwma.start(speed)
        pwmb.start(speed)
        sleep(0.02)
    else:
        GPIO.output(AIN1, GPIO.LOW)
        GPIO.output(AIN2, GPIO.HIGH)
        GPIO.output(BIN1, GPIO.HIGH)
        GPIO.output(BIN2, GPIO.LOW)
        pwma.start(speed)
        pwmb.start(speed)
        sleep(0.02)

def setServoAngle(servo, angle):
    assert angle >= 30 and angle <= 150
    pwm = GPIO.PWM(servo, 50)
    pwm.start(8)
    dutyCycle = angle / 18. + 3.
    pwm.ChangeDutyCycle(dutyCycle)
    sleep(0.02)
    pwm.stop()

# viewpoint rotation Y
def verAngle(angle):
    setServoAngle(VER, angle)

# vierpoint rotation X
def horAngle(angle):
    setServoAngle(HOR, angle)

    

# 停止工作
def stop():
    pwma.stop()
    pwmb.stop()
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.LOW)



if __name__ == "__main__":
    try:
        GPIO.output(STBY, GPIO.HIGH)
        while(True):
            try:

                option = input('control while spped (-100 ~ 100)')
                speed = 0
                if int(option) < -100: 
                    # testForward(-100)
                    speed = -100
                elif int(option) > 100:
                    speed = 100
                    # testForward(100)
                else:
                    print(option)
                    speed = int(option)

                goForward(speed)
           
            except ValueError:
                print('请输入正确的数字')




    except KeyboardInterrupt:
        stop()
        GPIO.cleanup()
    
