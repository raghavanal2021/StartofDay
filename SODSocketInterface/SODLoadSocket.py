from starlette.applications import Starlette
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

def startup():
    print ("Server is ON and ready to Serve...")
    


async def websocket_endpoint(websocket):
    await websocket.accept()
    while True:
        mesg = await websocket.receive_json()
        print(mesg)
        await websocket.send_text(mesg.replace("Client", "Server"))
    await websocket.close()
    
    
routes = [
          WebSocketRoute("/startofday", websocket_endpoint)
         ]

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'])
]
app = Starlette(debug=True, routes=routes, on_startup=[startup], middleware=middleware)
