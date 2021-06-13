from nameko.rpc import Rpc, rpc, RpcProxy

class ServiceGateway:
    name = "ServiceGateway"
    
    cprproxy = RpcProxy("CPR_Service")
    nrproxy = RpcProxy("NarrowRange_Service")
    patternproxy = RpcProxy("Pattern_service")
    
    def __init__(self):
        pass
    
    def getInputfromSocket(self, data):
        print(data)
    
    
    
    
    