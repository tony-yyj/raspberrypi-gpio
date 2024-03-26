from time import sleep
import RPi.GPIO as GPIO
from servo_motor import ServoMotor

GPIO.setmode(GPIO.BCM)

# 倾斜
VER= 25

GPIO.setup(VER, GPIO.OUT)
pwm = GPIO.PWM(VER, 50)



if __name__ == "__main__":
    try:
        verServoMotor = ServoMotor(pwm)
        while(True):
            try:

                option = input('control while angle (0 ~ 180):')
                data_angle = int(option)
                if int(option) < 0: 
                    angle = 0 
                elif int(option) > 180:
                    angle = 180
                else:
                    angle = int(option)

                verServoMotor.setServoAngle(angle)
           
            except ValueError:
                print('请输入正确的数字')




    except KeyboardInterrupt:
        del verServoMotor
        GPIO.cleanup()




