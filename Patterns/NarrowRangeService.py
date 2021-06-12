import json
from nameko.events import EventDispatcher, event_handler
from nameko.rpc import rpc
from Patterns.NarrowRangeAnalysis import NarrowRange


class NarrowRangeService(object):
    
    name = "NarrowRange_Service"
    
    @event_handler("StartofDay_Service","narrowrangeevent")
    @rpc
    def setnarrowrange(self,request):
        requestdata = json.loads(request)
        targetDate = requestdata["targetDate"]
        noofdays = 10
        rangepattern = NarrowRange(targetDate,noofdays)
        rangepattern.setNarrowRange()
        return "Success"