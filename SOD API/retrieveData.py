import pandas as pd
from pymongo import MongoClient
import json


class DataRetrieve():
    def __init__(self,target):
        print(target)
        self.connection = MongoClient('localhost',27017)
        self.db = self.connection['StartofDay']
        self.collection = self.db[target]
        
    def cpr(self):
        cprresult = self.collection.find( {"name":"cpr"},{"_id":0,"name":0 })
        result = pd.DataFrame(list(cprresult))
        return result.data[0]
    
    #data.to_json(orient='columns')
    def nr7(self):
        nr7result = self.collection.find({"name":"narrowrange7"},{"_id":0,"name":0 })
        result = pd.DataFrame(list(nr7result))
        return result.data[0]
    

    def nr4(self):
        nr7result = self.collection.find({"name":"narrowrange4"},{"_id":0,"name":0 })
        result = pd.DataFrame(list(nr7result))
        return result.data[0]
    
    def candles(self):
        candleresult = self.collection.find({"name":"candles"},{"_id":0,"name":0 })
        result = pd.DataFrame(list(candleresult))
        return result.data[0]