from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 水平
pan = 17

GPIO.setup(pan, GPIO.OUT)

def setServoAngle(servo, angle):
    assert angle >= 30 and angle <= 150
    pwm = GPIO.PWM(servo, 50)
    pwm.start(8)
    dutyCycle = angle / 18. + 3.
    pwm.ChangeDutyCycle(dutyCycle)
    sleep(0.3)
    pwm.stop()

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 0:
        setServoAngle(pan, 90)
    else:
        setServoAngle(pan, int(sys.argv[1]))


    GPIO.cleanup()



