from time import sleep
import pygame  
import logging  
import sys  
from prettytable import PrettyTable
from car_control import CarControl

logging.basicConfig(level=logging.DEBUG)  # 设置日志级别为DEBUG  


# 初始化pygame的joystick模块  
pygame.init()  
pygame.joystick.init()  
  
# 获取第一个连接的手柄（如果有的话）  
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]  
if not joysticks:  
    print("No joysticks found.")  
    sys.exit()  
  
joystick = joysticks[0]  
joystick.init()  

# 手柄名称
joystick_name = joystick.get_name()
print(f"joystick_name: {joystick_name}")

carControl = CarControl()

  
running = True
if __name__ == "__main__":

    try:

        direction = 'forward'
        while(running):
            try:
                for event in pygame.event.get():  
                    if event.type == pygame.QUIT:  
                        running = False  
            
                table =PrettyTable()

                stopButton = joystick.get_button(0)
                if (stopButton == 1):
                    carControl.stop()
                    continue


                directionLeftRight = joystick.get_axis(0)
                if directionLeftRight > 0.5:
                    carControl.turn_right()
                elif directionLeftRight < -0.5:
                    carControl.turn_left()
                    pass
                else:
                    carControl.straight_ahead()
                    pass

                directionForward = joystick.get_axis(1)
                if directionForward < -0.5:
                    carControl.move_forward()
                elif directionForward > 0.5:
                    carControl.move_backword()
                else:
                    pass


                speedButton = joystick.get_button(1)
                if speedButton == 1:
                    carControl.change_speed()
                else:
                    carControl.change_speed(True)


             
                sleep(0.1)

            except ValueError:
                pass




    except KeyboardInterrupt:
        pygame.quit()
        

