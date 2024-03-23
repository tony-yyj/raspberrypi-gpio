import asyncio
import websockets
import datetime

async def time_server(websocket):
    while True:
        # 加上时间戳 精确到毫秒
        dt_ms = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        print(dt_ms)
        await websocket.send(dt_ms)
        await asyncio.sleep(1 / 50)


async def start_server():
    websockets.serve(time_server, 'localhost', 5001)

loop = asyncio.get_event_loop()

loop.run_until_complete(start_server())
loop.run_forever()