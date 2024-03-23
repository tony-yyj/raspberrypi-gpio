import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

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

# 停止工作
def stop():
    pwma.stop()
    pwmb.stop()
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.LOW)

def testForward():
    goForward(100)



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
    
