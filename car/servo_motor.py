from time import sleep
from gpio_pin import GPIOPIN
import RPi.GPIO as GPIO

# sg90s 舵机
class ServoMotor:
    def __init__(self, pwm) -> None:
        self.pwm = pwm
        self.pwm.start(0)

    def __delattr__(self) -> None:
        pass


    @staticmethod
    def angleToDujtyCycle(num):
        fm = 10.0 / 180.0
        num = num * fm + 2.5
        num = int(num * 10) / 10.0
        return num
    
    def setServoAngle(self, angle):
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180
        else:
            pass

        dutyCycle = ServoMotor.angleToDujtyCycle(angle) 
        print(f"duty cycle: {dutyCycle}")
        self.pwm.ChangeDutyCycle(dutyCycle)
        sleep(0.1)
        self.pwm.ChangeDutyCycle(0)
        sleep(0.1)


class CameraServoMotor:

    @staticmethod
    def accAngle(preAngle, increment):
        angle = preAngle + increment
        if angle > 180:
            return 180
        elif angle < 0:
            return 0
        else:
            return angle

    def __init__(self) -> None:
        self.__verAngle = 75
        self.__horAngle = 75
        GPIO.setup(GPIOPIN.HOR_SERVO_PIN(), GPIO.OUT)
        GPIO.setup(GPIOPIN.VER_SERVO_PIN(), GPIO.OUT)
        pwmVer = GPIO.PWM(GPIOPIN.VER_SERVO_PIN(), 50)
        pwmHor = GPIO.PWM(GPIOPIN.HOR_SERVO_PIN(), 50)
        self.__horMotor= ServoMotor(pwmHor)
        self.__verMotor= ServoMotor(pwmVer)
        self.__horMotor.setServoAngle(self.__horAngle)
        self.__verMotor.setServoAngle(self.__verAngle)
    
    def moveVerMotorDown(self):
        self.__verAngle = CameraServoMotor.accAngle(self.__verAngle, 10)
        self.__verMotor.setServoAngle(self.__verAngle)
        
    def moveVerMotorUp(self):
        self.__verAngle = CameraServoMotor.accAngle(self.__verAngle, - 10)
        self.__verMotor.setServoAngle(self.__verAngle)


    def moveHorMotorLeft(self):
        self.__horAngle = CameraServoMotor.accAngle(self.__horAngle, + 10)
        self.__horMotor.setServoAngle(self.__horAngle)

    def moveHorMotorRight(self):
        self.__horAngle = CameraServoMotor.accAngle(self.__horAngle, - 10)
        self.__horMotor.setServoAngle(self.__horAngle)

