import time from sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def setServoAngle(servo, angle):
    assert angle > 30 and angle <=150
    pwm = GPIO.PWM(servo, 50)
    pwm.start(8)
    currentlyAngle = 180 - angle
