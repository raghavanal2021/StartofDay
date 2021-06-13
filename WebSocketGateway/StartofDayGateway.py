import json
from datetime import datetime
from nameko.standalone.rpc import ClusterRpcProxy
import numpy as np
import pandas as pd
from models.ResponseContract import AuditResponse
import datetime;



class StartofDay:
    def __init__(self):
        self.config = { 'AMQP_URI': 'pyamqp://guest:guest@localhost'}
        
    def callcprServices(self, payload):
        with ClusterRpcProxy(self.config) as cluster_rpc:
            try:
                cpr_res = cluster_rpc.CPR_Service.processCPR.call_async(payload)
                response = AuditResponse(event='CPR Status',timestamp = datetime.datetime.now().isoformat() ,status = cpr_res.result(),description=f"CPR for payload {payload} completed successfully ",errorcode = None,errorDesc = None).audit()
                print(response)
            except Exception as e:
                response = AuditResponse(event='CPR Status',timestamp = datetime.datetime.now().isoformat() ,status = cpr_res.result(),description=f"CPR for payload {payload} errored ",errorcode = e ,errorDesc = e).audit()
        return response
    
    def callnarrowrangeServices(self,payload):
        with ClusterRpcProxy(self.config) as cluster_rpc:
            try:
                narrowrange = cluster_rpc.NarrowRange_Service.setnarrowrange.call_async(payload)
                response = AuditResponse(event='Narrow Range Status',timestamp = datetime.datetime.now().isoformat() ,status = narrowrange.result(),description=f"Narrow Range for payload {payload} completed successfully ",errorcode = None,errorDesc = None).audit()
                print(response)
            except Exception as e:
                response = AuditResponse(event='Narrow Range Status',timestamp = datetime.datetime.now().isoformat() ,status = narrowrange.result(),description=f"Narrow Range for payload {payload} errored ",errorcode = e ,errorDesc = e).audit()
        return response
    
    def callPatternServices(self,payload):
        with ClusterRpcProxy(self.config) as cluster_rpc:
            try:
                pattern = cluster_rpc.Pattern_Service.setPattern.call_async(payload)
                response = AuditResponse(event='Pattern Analysis Status',timestamp = datetime.datetime.now().isoformat() ,status = pattern.result(),description=f"Pattern Analysis for payload {payload} completed successfully ",errorcode = None,errorDesc = None).audit()
                print(response)
            except Exception as e:
                response = AuditResponse(event='Pattern Analysis Status',timestamp = datetime.datetime.now().isoformat() ,status = pattern.result(),description=f"Pattern Analysis for payload {payload} errored ",errorcode = e ,errorDesc = e).audit()
        return pattern.result()
    


if __name__ == '__main__':
    sod = StartofDay()
    sod.callcprServices('{"targetDate": "20210107", "noofdays": 10}')
    sod.callnarrowrangeServices('{"targetDate": "20210107", "noofdays": 10}')
    sod.callPatternServices('{"targetDate": "20210107", "noofdays": 10}')
    


            
    
    
    
        
        
