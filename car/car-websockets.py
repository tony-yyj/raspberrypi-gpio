import asyncio  
import websockets  
import logging  
import json
import signal  

import RPi.GPIO as GPIO
from time import sleep
from servo_motor import ServoMotor

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
pwmVer = GPIO.PWM(VER, 50)
pwmHor = GPIO.PWM(HOR, 50)
# ----------------


verServoMotor = ServoMotor(pwmVer)
horServoMotor = ServoMotor(pwmHor)


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

def accAngle(preAngle, increment):
    angle = preAngle + increment
    if angle > 180:
        return 180
    elif angle < 0:
        return 0
    else:
        return angle

async def echo(websocket, path):  
    try:  
        async for message in websocket:  
            global global_horAngle
            global global_verAngle
            global verServoMotor
            global horServoMotor
            logging.debug(f"Received message: {message}")  
            data = json.loads(message)
            if data['topic'] == 'camera':
                if data['direction'] == 'left':
                    global_horAngle= accAngle(global_horAngle, 10)
                    horServoMotor.setServoAngle(global_horAngle)
                    response = json.dumps({'message': 'received', 'hor_angle':global_horAngle})
                    await websocket.send(response)

                elif data['direction'] == 'right':
                    global_horAngle= accAngle(global_horAngle, - 10)
                    horServoMotor.setServoAngle(global_horAngle)
                    response = json.dumps({'message': 'received', 'hor_angle':global_horAngle})
                    await websocket.send(response)

                elif data['direction'] == 'up':
                    global_verAngle= accAngle(global_verAngle, - 10)
                    verServoMotor.setServoAngle(global_verAngle)
                    response = json.dumps({'message': 'received', 'ver_angle':global_verAngle})
                    await websocket.send(response)
                elif data['direction'] == 'down':
                    global_verAngle= accAngle(global_verAngle,  10)
                    verServoMotor.setServoAngle(global_verAngle)
                    response = json.dumps({'message': 'received', 'ver_angle':global_verAngle})
                    await websocket.send(response)
                else:
                    pass

            if data['topic'] == 'wheel':
                data_speed = int(data['speed'])
                if data['direction'] == 'front':
                    speed = data_speed
                    goForward(speed)
                elif data['direction'] == 'back':
                    speed = 0 - data_speed
                    goForward(speed)
                elif data['direction'] == 'left':
                    speed = data_speed
                    changeDirection(speed)
                elif data['direction'] == 'right':
                    speed = 0 - data_speed
                    changeDirection(speed)
                elif data['direction'] == 'stop': 
                    stop()
                else:
                    pass

                response = json.dumps({'message': 'received', 'global_speed':data_speed})
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
    global verServoMotor
    global horServoMotor
    horServoMotor.setServoAngle(global_horAngle)
    verServoMotor.setServoAngle(global_verAngle)
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
    stop()
    print('shut down car')
    GPIO.cleanup()
    loop.close()
