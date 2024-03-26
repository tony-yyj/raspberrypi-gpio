import asyncio  
import websockets  
import logging  
import json
import signal  

import RPi.GPIO as GPIO
from time import sleep
from car_motor import CarMotor
from servo_motor import CameraServoMotor

GPIO.setwarnings(False)


GPIO.setmode(GPIO.BCM)


carMotor = CarMotor()
cameraMotor = CameraServoMotor()


logging.basicConfig(level=logging.DEBUG)  # 设置日志级别为DEBUG  

async def carServer(websocket, path):  
    try:  
        async for message in websocket:  
            global carMotor
            global cameraMotor
            logging.debug(f"Received message: {message}")  
            data = json.loads(message)
            if data['topic'] == 'camera':
                if data['direction'] == 'left':
                    cameraMotor.moveHorMotorLeft()

                elif data['direction'] == 'right':
                    cameraMotor.moveHorMotorRight()

                elif data['direction'] == 'up':
                    cameraMotor.moveVerMotorUp()
                elif data['direction'] == 'down':
                    cameraMotor.moveVerMotorDown()
                else:
                    pass

            if data['topic'] == 'wheel':
                speed = int(data['speed'])
                if data['direction'] == 'front':
                    carMotor.forwoard(speed)
                elif data['direction'] == 'back':
                    carMotor.back(speed)
                elif data['direction'] == 'left':
                    carMotor.turnLeft(speed)
                elif data['direction'] == 'right':
                    carMotor.turnRight(speed)
                elif data['direction'] == 'stop': 
                    carMotor.stop()
                else:
                    pass

                response = json.dumps({'message': 'received', 'speed': speed})
                await websocket.send(response)


    except json.JSONDecodeError:
        await websocket.send(json.dumps({'error', 'invalid JSON format'}))
    except websockets.exceptions.ConnectionClosed as e:  
        carMotor.stop()
        logging.warning(f"WebSocket connection closed: {e}")  
    except Exception as e:  
        logging.error(f"An error occurred: {e}")  
        # 你可以选择在这里进行更复杂的错误处理，比如重新连接等  

async def main():  
    async with websockets.serve(carServer, "192.168.0.111", 8765):  
        print("Server started on port 8765")  
        try:  
            await asyncio.Future()  # 这将永远等待，直到被取消  
        except asyncio.CancelledError:  
            pass  

  
 # 设置信号处理器  
def stop_server(loop):  
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]  
    [task.cancel() for task in tasks]  
    global carMotor
    carMotor.stop
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
    print('shut down car')
    GPIO.cleanup()
    loop.close()
