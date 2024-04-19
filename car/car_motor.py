import RPi.GPIO as GPIO
from time import sleep
from gpio_pin import GPIOPIN

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class CarMotor:
    def __init__(self) -> None:
        GPIO.setup(GPIOPIN.STBY(), GPIO.OUT)
        GPIO.setup(GPIOPIN.PWMA(), GPIO.OUT)
        GPIO.setup(GPIOPIN.AIN1(), GPIO.OUT)
        GPIO.setup(GPIOPIN.AIN2(), GPIO.OUT)

        GPIO.setup(GPIOPIN.PWMB(), GPIO.OUT)
        GPIO.setup(GPIOPIN.BIN1(), GPIO.OUT)
        GPIO.setup(GPIOPIN.BIN2(), GPIO.OUT)
        GPIO.output(GPIOPIN.STBY(), GPIO.HIGH)
        self.pwmLeft = GPIO.PWM(GPIOPIN.PWMA(), 300)
        self.pwmRight = GPIO.PWM(GPIOPIN.PWMB(), 300)
        self.speed_rate = 1
        self.MAX_SPEED = 60
        self.speed = 0
    
    def accelerate(self, movement, direction, dec = False, rate = 0):
        speed_rate = self.speed_rate
        if dec:
            speed_rate = (self.speed_rate + rate) * -1
        
        self.speed = self.speed + speed_rate

        if self.speed >= self.MAX_SPEED:
            self.speed = self.MAX_SPEED 
        elif self.speed < 0:
            self.speed = 0

        if movement == 'forward' or movement == 'backward':
            leftSpeed = self.speed
            rightSpeed = self.speed
            if direction == 'left':
                leftSpeed = 0
            elif direction == 'right':
                rightSpeed = 0


            self.pwmLeft.start(leftSpeed)
            self.pwmRight.start(rightSpeed)
        else:
            self.pwmLeft.start(0)
            self.pwmRight.start(0)

        sleep(0.01)
        

        
    def getSpeed(self):
        return self.speed


    def forwoard(self):
        GPIO.output(GPIOPIN.AIN1(), GPIO.LOW)
        GPIO.output(GPIOPIN.AIN2(), GPIO.HIGH)
        GPIO.output(GPIOPIN.BIN1(), GPIO.LOW)
        GPIO.output(GPIOPIN.BIN2(), GPIO.HIGH)
        sleep(0.001)
    
    def backward(self):
        GPIO.output(GPIOPIN.AIN1(), GPIO.HIGH)
        GPIO.output(GPIOPIN.AIN2(), GPIO.LOW)
        GPIO.output(GPIOPIN.BIN1(), GPIO.HIGH)
        GPIO.output(GPIOPIN.BIN2(), GPIO.LOW)
        sleep(0.001)
    
    def stop(self):
        self.speed = 0
        self.pwmLeft.stop()
        self.pwmRight.stop()
        GPIO.output(GPIOPIN.AIN1(), GPIO.LOW)
        GPIO.output(GPIOPIN.AIN2(), GPIO.LOW)
        GPIO.output(GPIOPIN.BIN1(), GPIO.LOW)
        GPIO.output(GPIOPIN.BIN2(), GPIO.LOW)
    
    def __delattr__(self, __name: str) -> None:
        self.stop()
        

