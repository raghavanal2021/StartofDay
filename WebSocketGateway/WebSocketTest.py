import asyncio
import websockets

async def hello(websocket,path):
    name = await websocket.recv()
    print(f"{name}")
    greeting = f"Hello{name}!"
    