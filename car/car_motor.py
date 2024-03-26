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

    def forwoard(self, speed):
        GPIO.output(GPIOPIN.AIN1(), GPIO.LOW)
        GPIO.output(GPIOPIN.AIN2(), GPIO.HIGH)
        GPIO.output(GPIOPIN.BIN1(), GPIO.LOW)
        GPIO.output(GPIOPIN.BIN2(), GPIO.HIGH)
        print(f'speed:{speed}')
        self.pwmLeft.start(speed)
        self.pwmRight.start(speed)
        sleep(0.02)
    
    def back(self, speed):
        GPIO.output(GPIOPIN.AIN1(), GPIO.HIGH)
        GPIO.output(GPIOPIN.AIN2(), GPIO.LOW)
        GPIO.output(GPIOPIN.BIN1(), GPIO.HIGH)
        GPIO.output(GPIOPIN.BIN2(), GPIO.LOW)
        self.pwmLeft.start(speed)
        self.pwmRight.start(speed)
        sleep(0.02)
    
    def turnLeft(self, speed):
        # 左侧speed减半实现左转
        GPIO.output(GPIOPIN.AIN1(), GPIO.HIGH)
        GPIO.output(GPIOPIN.AIN2(), GPIO.LOW)
        GPIO.output(GPIOPIN.BIN1(), GPIO.LOW)
        GPIO.output(GPIOPIN.BIN2(), GPIO.HIGH)
        self.pwmLeft.start(speed)
        self.pwmRight.start(speed)
        sleep(0.02) 

    def turnRight(self, speed):
        # 右侧侧speed减半实现右转
        GPIO.output(GPIOPIN.AIN1(), GPIO.LOW)
        GPIO.output(GPIOPIN.AIN2(), GPIO.HIGH)
        GPIO.output(GPIOPIN.BIN1(), GPIO.HIGH)
        GPIO.output(GPIOPIN.BIN2(), GPIO.LOW)
        self.pwmLeft.start(speed)
        self.pwmRight.start(speed / 2)
        sleep(0.02) 
    
    def stop(self):
        self.pwmLeft.stop()
        self.pwmRight.stop()
        GPIO.output(GPIOPIN.AIN1(), GPIO.LOW)
        GPIO.output(GPIOPIN.AIN2(), GPIO.LOW)
        GPIO.output(GPIOPIN.BIN1(), GPIO.LOW)
        GPIO.output(GPIOPIN.BIN2(), GPIO.LOW)
    
    def __delattr__(self, __name: str) -> None:
        self.stop()
        

