import json
from nameko.events import EventDispatcher, event_handler
from nameko.rpc import rpc
from nameko_http.exceptions import HttpError
from PatternImpl import ImplementPattern
import eventlet.tpool
import numpy as np

class PricePattern(object):
    
    name = "Pattern_Service"
    
    
    @event_handler("StartofDay_Service","patternevent")
    @rpc
    def setPattern(self,request):
        return eventlet.tpool.execute(self._pattern,request)
        
        
        
        
    def _pattern(self,request):
        requestdata = json.loads(request)
        print(requestdata)
        targetDate = requestdata["targetDate"]
        noofdays = requestdata["noofdays"]
        pattern = ImplementPattern(targetDate,noofdays)    
        df = pattern.setPattern()
        return "Success"
    
        
    
    '''
    @api('POST','/startofday/getNarrowRange',cors_enabled=True)
    def getBullishPattern(self,request):
        requestdata = json.loads(request.data.decode("utf-8"))
        targetDate = requestdata["targetDate"]
        rangepattern = NarrowRange(targetDate,14)
        df = rangepattern.getNarrowRange7()
        return Response(df.to_json(orient='records',date_format='iso'))
    
    '''