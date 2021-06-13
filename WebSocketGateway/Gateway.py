import socketio
from nameko.standalone.rpc import ClusterRpcProxy
import json

config = {
    'AMQP_URI': 'pyamqp://guest:guest@localhost'
}

sio = socketio.AsyncServer( async_mode='asgi', cors_allowed_origins='*')
app = socketio.ASGIApp(sio)

@sio.event
async def connect(sid, environ, auth):
    print ('Client Connected ' + sid)
    await sio.emit('status',{'status':'Client Connected', 'event':'Connect Event'})
    
@sio.event
async def disconnect(sid):
    print ('Client Disconnected '  + sid)
    
@sio.event
async def startofday(sid,data):
    print("Data received from Server " + data)
    requestdata = json.loads(data)
    print(requestdata["startdate"])    
    await sio.emit('status', 'Received Data from server ' + data)
    
    
def processdata(data):
    with ClusterRpcProxy(config) as cluster_rpc:
        pass
    