from time import sleep

# sg90s 舵机
class ServoMotor:
    def __init__(self, pwm) -> None:
        self.pwm = pwm
        self.pwm.start(0)

    def __delattr__(self) -> None:
        self.pwm.stop(0)


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
        sleep(0.3)
        self.pwm.ChangeDutyCycle(0)
        sleep(0.1)





