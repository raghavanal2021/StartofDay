import json
from datetime import datetime
import pandas as pd
from models.InputPayload import PayloadContract
from models.ServiceContract import ServiceContract


class Utilities:
    
    def __init__(self):
        pass
    
    def parsepayload(self,payload):
        requestdata = json.loads(payload)
        startDate = datetime.strptime(requestdata["startdate"],'%Y%m%d')
        endDate = datetime.strptime(requestdata["enddate"],'%Y%m%d')
        resolution = requestdata["noofdays"]
        contract = PayloadContract()
        contract.setStartDate(startDate)
        contract.setendDate(endDate)
        contract.setnoofdays(resolution)
        return contract
            
    def getBusinessDates(self, startDate, endDate):
        df  = pd.DataFrame(pd.bdate_range(start=startDate, end=endDate))
        return (df[0].dt.strftime('%Y%m%d')).tolist()
        
    def runningcontract(self, payloadContract):
        inputcontract:PayloadContract  = self.parsepayload(payloadContract)
        daterange = self.getBusinessDates(inputcontract.getStartDate(), inputcontract.getendDate())
        servicecontracts = []
        for dates in daterange:
            scontract = ServiceContract()
            scontract.setTargetDate(dates)
            scontract.setnoofdays(inputcontract.getnoofdays())
            servicecontracts.append(scontract.__dict__)
       # print(servicecontracts)
        return servicecontracts
            
'''
if __name__ == '__main__':
    util = Utilities()
    util.runningcontract('{"startdate":"20210104","enddate":"20210131","noofdays":15} ')
'''
