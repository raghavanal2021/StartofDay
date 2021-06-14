import socketio
from nameko.standalone.rpc import ClusterRpcProxy
import json
from models.ResponseContract import AuditResponse
import datetime
from utilities import Utilities
from StartofDayGateway import StartofDay

config = {
    'AMQP_URI': 'pyamqp://guest:guest@localhost'
}

sio = socketio.AsyncServer( async_mode='asgi', cors_allowed_origins='*')
app = socketio.ASGIApp(sio)

@sio.event
async def connect(sid, environ, auth):
    print ('Client Connected ' + sid)
    response = AuditResponse(event='Connection',timestamp = datetime.datetime.now().isoformat() ,status = "Connected",description=f"Connection established with Server ",errorcode = None ,errorDesc = None).audit()
    await sio.emit('connect',response)

@sio.event
async def heartbeat(sid,data):
    await sio.emit(data)
    
@sio.event
async def startofday(sid,data):
    print("Data received from Server " + data)
    requestdata = json.loads(data)
    start = requestdata["startdate"]
    end = requestdata["enddate"]
    response = AuditResponse(event='loadstart',timestamp = datetime.datetime.now().isoformat() ,status = "Started",description=f"Load started for the requested dates {start} and {end} ",errorcode = None ,errorDesc = None).audit()
    await sio.emit('loadstart',response)
    loadlist = processdata(data)
    sodload = StartofDay()
    for loaddate in loadlist:
        print(loaddate)
        response = AuditResponse(event='CPR Status',timestamp = datetime.datetime.now().isoformat() ,status = "Started",description=f"CPR Load started for the payload {loaddate} ",errorcode = None ,errorDesc = None).audit()
        await sio.emit('loadstatus',response)
        response = sodload.callcprServices(json.dumps(loaddate))
        await sio.emit('loadstatus',response)
        
        response = AuditResponse(event='Narrow Range Status',timestamp = datetime.datetime.now().isoformat() ,status = "Started",description=f"Narrow Range Load started for the payload {loaddate} ",errorcode = None ,errorDesc = None).audit()
        await sio.emit('loadstatus',response)
        response = sodload.callnarrowrangeServices(json.dumps(loaddate))
        await sio.emit('loadstatus',response)
        
        response = AuditResponse(event='Technical Pattern Status',timestamp = datetime.datetime.now().isoformat() ,status = "Started",description=f"Technical Pattern Load started for the payload {loaddate} ",errorcode = None ,errorDesc = None).audit()
        await sio.emit('loadstatus',response)
        response = sodload.callPatternServices(json.dumps(loaddate))
        await sio.emit('loadstatus',response)
        
        
    response = AuditResponse(event='loadend',timestamp = datetime.datetime.now().isoformat() ,status = "Started",description=f"Load started for the requested dates {start} and {end} ",errorcode = None ,errorDesc = None).audit()
    await sio.emit('loadend',response)
        
    
def processdata(data):
    util = Utilities()
    return util.runningcontract(data)