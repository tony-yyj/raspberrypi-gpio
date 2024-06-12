import RPi.GPIO as GPIO

import time

GPIO.setmode(GPIO.BCM)

PIN = 18

GPIO.setup(PIN, GPIO.OUT)

def blink(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(1)
    return


def main():
    for i in range(0, 50):
        blink(PIN)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
        pass