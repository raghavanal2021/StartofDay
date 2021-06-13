class AuditResponse(object):
    
    def __init__(self,event,timestamp,status,description,errorcode,errorDesc):
        self.event =  event
        self.timestamp = timestamp
        self.status = status
        self.description = description
        self.errorcode = errorcode
        self.errorDesc = errorDesc
        
    
    def audit(self):
        return ({'event':self.event,'timestamp':self.timestamp,'status':self.status, 'description':self.description, 'errorcode':self.errorcode, 'self.errorDesc':self.errorDesc})
        