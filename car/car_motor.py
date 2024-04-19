import RPi.GPIO as GPIO
from time import sleep
from gpio_pin import GPIOPIN



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
        self.speed = 0
        self.DIRECTIAN = {
            'forward': self.forwoard,
            'back': self.back,
            'left': self.turnLeft,
            'right': self.turnRight,
        }
    
    def accelerate(self, direction, dec = False):
        self.speed = self.speed + (-1 if dec else 1 )
        if self.speed > 100:
            self.speed = 99
        elif self.speed < 0:
            self.speed = 0

        for _direction in self.DIRECTIAN:
            if _direction == direction:
                handle = self.DIRECTIAN[_direction]
                handle()
                return
        
    def getSpeed(self):
        return self.speed


    def forwoard(self):
        GPIO.output(GPIOPIN.AIN1(), GPIO.LOW)
        GPIO.output(GPIOPIN.AIN2(), GPIO.HIGH)
        GPIO.output(GPIOPIN.BIN1(), GPIO.LOW)
        GPIO.output(GPIOPIN.BIN2(), GPIO.HIGH)
        self.pwmLeft.start(self.speed)
        self.pwmRight.start(self.speed)
        sleep(0.001)
    
    def back(self):
        GPIO.output(GPIOPIN.AIN1(), GPIO.HIGH)
        GPIO.output(GPIOPIN.AIN2(), GPIO.LOW)
        GPIO.output(GPIOPIN.BIN1(), GPIO.HIGH)
        GPIO.output(GPIOPIN.BIN2(), GPIO.LOW)
        self.pwmLeft.start(self.speed)
        self.pwmRight.start(self.speed)
        sleep(0.001)
    
    def turnLeft(self):
        # 左侧speed减半实现左转
        self.pwmLeft.start(self.speed / 2)
        self.pwmRight.start(self.speed)
        sleep(0.001) 

    def turnRight(self):
        # 右侧侧speed减半实现右转
        self.pwmLeft.start(self.speed)
        self.pwmRight.start(self.speed / 2)
        sleep(0.001) 
    
    def stop(self):
        self.speed = 0
        self.direction = 'forward'
        self.pwmLeft.stop()
        self.pwmRight.stop()
        GPIO.output(GPIOPIN.AIN1(), GPIO.LOW)
        GPIO.output(GPIOPIN.AIN2(), GPIO.LOW)
        GPIO.output(GPIOPIN.BIN1(), GPIO.LOW)
        GPIO.output(GPIOPIN.BIN2(), GPIO.LOW)
    
    def __delattr__(self, __name: str) -> None:
        self.stop()
        

