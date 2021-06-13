
from nameko.events import EventDispatcher, event_handler
from nameko.rpc import rpc
import json

class DayStart():
    name = "StartofDay_Service"
    
    ''' Set Event Dispatcher '''
    dispatch = EventDispatcher()
    event_name = 'cprevent'
    ptn_event_name = 'patternevent'
    nr_event_name = 'narrowrangeevent'
                              
    @rpc
    def setstartofday(self,targetDates,noofdays):
        payloaddict = {"targetDate": targetDates, "noofdays":noofdays}
        payload = json.dumps(payloaddict)
        self.sendcprevent(payload)
        self.sendnrevent(payload)
        self.sendptrnevent(payload)
        
    def sendcprevent(self,payload):
        self.dispatch(self.event_name,payload)
        
     
    def sendnrevent(self,payload):
        self.dispatch(self.nr_event_name,payload)   
        
    def sendptrnevent(self,payload):
        self.dispatch(self.ptn_event_name,payload)
     
        
        
    