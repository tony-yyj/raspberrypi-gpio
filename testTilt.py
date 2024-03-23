from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# 倾斜
tilt = 25

GPIO.setup(tilt, GPIO.OUT)

def setServoAngle(servo, angle):
    assert angle >= 30 and angle <= 150
    pwm = GPIO.PWM(servo, 50)
    pwm.start(8)
    currentlyAngle = 180 - angle
    dutyCycle = currentlyAngle / 18. + 3.
    pwm.ChangeDutyCycle(dutyCycle)
    sleep(0.3)
    pwm.stop()

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 0:
        setServoAngle(tilt, 90)
    else:
        setServoAngle(tilt, int(sys.argv[1]))


    GPIO.cleanup()


