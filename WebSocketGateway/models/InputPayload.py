class PayloadContract:
    
    def __init__(self):
        self.startDate = None
        self.endDate = None
        self.noofDays = None
        
    
    def getStartDate(self):
        return self.startDate
    
    def setStartDate(self, startDate):
        self.startDate = startDate
    
    def getendDate(self):
        return self.endDate
    
    def setendDate(self,endDate):
        self.endDate = endDate
        
    def getnoofdays(self):
        return self.noofDays
    
    def setnoofdays(self,noofdays):
        self.noofDays = noofdays
        
        