import json
from nameko.events import EventDispatcher, event_handler
from nameko.rpc import rpc
from CPRImpl import CPRImplementation
import numpy as np

class CPRCalc:
    name = "CPR_Service"
    
    ''' Set the event dispatcher '''
    dispatch = EventDispatcher()
    
    def __init__(self):
        pass
    
    @event_handler("StartofDay_Service","cprevent")
    @rpc
    def processCPR(self,pattern): 
        response = json.loads(pattern)
        targetDate = response['targetDate']
        noofdays = response['noofdays']  
        cpr = CPRImplementation(targetDate,noofdays)
        cprdf = cpr.pivotCalculation()
        pointsdf = cpr.camarillapoints(cprdf)
        latestrecord = cpr.returnlatest(targetDate)
        return "Success"
    