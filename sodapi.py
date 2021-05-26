from CPR.CPRService import CPRCalc
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

@app.get("/")
async def healthCheck():
        return {"health":"GREEN","health Info": "Application running successfully..."}

class RequestBody(BaseModel):
    targetDate:str
    noofdays:str
    nrange:Optional[str] = None
    
@app.post("/cpr")
async def postCPR(request: RequestBody):
    ,