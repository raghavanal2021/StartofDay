from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.routing import request_response
from retrieveData import DataRetrieve
from nameko.events import EventDispatcher, event_handler
from nameko.rpc import rpc, RpcProxy
import uvicorn


app = FastAPI()

origins = ["*"]
start = RpcProxy("StartofDay")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def healthCheck():
        return {"health":"GREEN","health Info": "Application running successfully..."}

class RequestBody(BaseModel):
    targetDate:str
    noofdays:str
    nrange:Optional[str] = None
    
@app.post("/cpr")
async def cpr(request : RequestBody):
        cprdata = DataRetrieve(request.targetDate)
        return cprdata.cpr()

@app.post("/nr7")
async def nr7(request : RequestBody):
        nr7data = DataRetrieve(request.targetDate)
        return nr7data.nr7()


@app.post("/nr4")
async def nr4(request : RequestBody):
        nr4data = DataRetrieve(request.targetDate)
        return nr4data.nr4()

@app.post("/candles")
async def candles(request : RequestBody):
        candledata = DataRetrieve(request.targetDate)
        return candledata.candles()


@app.post("/runService")
async def runService(request: RequestBody):
        return start.setstartofday(request.targetDate,request.noofdays)
        
if __name__ == "__main__":
        uvicorn.run(app, host="localhost",port=8085)