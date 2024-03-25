import asyncio  
import websockets  
import logging  
import json
import signal  

import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)

global_verAngle = 75
global_horAngle = 75

GPIO.setmode(GPIO.BCM)


# --- TB6612FNG ----
STBY = 27
PWMA = 18
AIN1 = 14
AIN2 = 15
PWMB = 19
BIN1 = 23
BIN2 = 24

GPIO.setup(STBY, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)

GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)

pwma = GPIO.PWM(PWMA, 300)
pwmb = GPIO.PWM(PWMB, 300)
# ----------------

# --- SG90s ---

# vertical axis Y
VER = 25
# horizontal axis X
HOR = 17

GPIO.setup(VER, GPIO.OUT)
GPIO.setup(HOR, GPIO.OUT)
# ----------------





# 前进或后退（大于0前进，小于0后退）
def goForward(speed):
    if (speed >= 0):
        GPIO.output(AIN1, GPIO.LOW)
        GPIO.output(AIN2, GPIO.HIGH)
        GPIO.output(BIN1, GPIO.LOW)
        GPIO.output(BIN2, GPIO.HIGH)
        pwma.start(speed)
        pwmb.start(speed)
        sleep(0.02)
    else:
        GPIO.output(AIN1, GPIO.HIGH)
        GPIO.output(AIN2, GPIO.LOW)
        GPIO.output(BIN1, GPIO.HIGH)
        GPIO.output(BIN2, GPIO.LOW)
        pwma.start(-speed)
        pwmb.start(-speed)
        sleep(0.02)

def changeDirection(speed):
    if (speed > 0):
        GPIO.output(AIN1, GPIO.HIGH)
        GPIO.output(AIN2, GPIO.LOW)
        GPIO.output(BIN1, GPIO.LOW)
        GPIO.output(BIN2, GPIO.HIGH)
        pwma.start(speed)
        pwmb.start(speed)
        sleep(0.02)
    else:
        GPIO.output(AIN1, GPIO.LOW)
        GPIO.output(AIN2, GPIO.HIGH)
        GPIO.output(BIN1, GPIO.HIGH)
        GPIO.output(BIN2, GPIO.LOW)
        pwma.start(-speed)
        pwmb.start(-speed)
        sleep(0.02)

def setServoAngle(servo, angle):
    assert angle >= 30 and angle <= 150
    pwm = GPIO.PWM(servo, 50)
    pwm.start(8)
    dutyCycle = angle / 18. + 3.
    pwm.ChangeDutyCycle(dutyCycle)
    sleep(0.02)
    pwm.stop()

# viewpoint rotation Y
def setVerAngle(angle):
    setServoAngle(VER, angle)

# vierpoint rotation X
def setHorAngle(angle):
    setServoAngle(HOR, angle)

    

# 停止工作
def stop():
    pwma.stop()
    pwmb.stop()
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.LOW)

logging.basicConfig(level=logging.DEBUG)  # 设置日志级别为DEBUG  

global_speed = 30
  
async def echo(websocket, path):  
    try:  
        async for message in websocket:  
            global global_horAngle
            global global_verAngle
            logging.debug(f"Received message: {message}")  
            data = json.loads(message)
            if data['topic'] == 'camera':
                if data['direction'] == 'right':
                    global_horAngle= global_horAngle+ 10
                    if (global_horAngle>= 150):
                        global_horAngle= 150
                    setHorAngle(global_horAngle)
                    response = json.dumps({'message': 'received', 'hor_angle':global_horAngle})
                    await websocket.send(response)

                elif data['direction'] == 'left':
                    global_horAngle= global_horAngle - 10
                    if (global_horAngle <= 30):
                        global_horAngle= 30
                    setHorAngle(global_horAngle)
                    response = json.dumps({'message': 'received', 'hor_angle':global_horAngle})
                    await websocket.send(response)

                elif data['direction'] == 'up':
                    global_verAngle= global_verAngle- 10
                    if (global_verAngle <= 30):
                        global_verAngle = 30
                    setVerAngle(global_verAngle)
                    response = json.dumps({'message': 'received', 'ver_angle':global_verAngle})
                    await websocket.send(response)
                elif data['direction'] == 'down':
                    global_verAngle= global_verAngle + 10
                    if (global_verAngle >=150):
                        global_verAngle = 150 
                    setVerAngle(global_verAngle)
                    response = json.dumps({'message': 'received', 'ver_angle':global_verAngle})
                    await websocket.send(response)
                else:
                    pass

            if data['topic'] == 'wheel':
                global global_speed
                if data['direction'] == 'front':
                    global_speed = 30
                    goForward(global_speed)
                elif data['direction'] == 'back':
                    global_speed = -30
                    goForward(global_speed)
                elif data['direction'] == 'left':
                    changeDirection(20)
                elif data['direction'] == 'right':
                    changeDirection(-20)
                elif data['direction'] == 'stop': 
                    stop()
                else:
                    pass

                response = json.dumps({'message': 'received', 'global_speed':global_speed})
                await websocket.send(response)


    except json.JSONDecodeError:
        await websocket.send(json.dumps({'error', 'invalid JSON format'}))
    except websockets.exceptions.ConnectionClosed as e:  
        stop()
        logging.warning(f"WebSocket connection closed: {e}")  
    except Exception as e:  
        logging.error(f"An error occurred: {e}")  
        # 你可以选择在这里进行更复杂的错误处理，比如重新连接等  

async def main():  
    setHorAngle(global_horAngle)
    setVerAngle(global_verAngle)
    async with websockets.serve(echo, "192.168.0.111", 8765):  
        print("Server started on port 8765")  
        try:  
            await asyncio.Future()  # 这将永远等待，直到被取消  
        except asyncio.CancelledError:  
            pass  

  
 # 设置信号处理器  
def stop_server(loop):  
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]  
    [task.cancel() for task in tasks]  
    stop()
    loop.stop()  


loop = asyncio.get_event_loop()  

# 添加信号处理器  
for sig in (signal.SIGINT, signal.SIGTERM):  
    loop.add_signal_handler(sig, lambda: stop_server(loop))  
  
try:  
    loop.run_until_complete(main())  
except KeyboardInterrupt:  
    pass  
finally:  
    loop.close()
