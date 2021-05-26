from DataFeed.SymbolFeed import EndofDayFeedSymbol
from DataFeed.Feed import EndofDayFeed
from pymongo import MongoClient
import json
import pandas as pd
import talib as tl
import os.path

class NarrowRange():
    
        def __init__(self,target,noofdays):
          self.target = target
          self.masterlist = EndofDayFeedSymbol().getMaster()
          self.eodlist = EndofDayFeed().getData(target, noofdays)
          self.symboldf = pd.DataFrame()
          self.outputdf = pd.DataFrame()
          
        def setNarrowRange(self):
            data = self.masterlist
            symboldata = self.eodlist
            symbollist = data['master_symbol'].tolist()
            for symbol in symbollist:
                try:
                    self.symboldf = symboldata[(symboldata['symbol'] == symbol)]
                    self.symboldf = self.symboldf.reset_index()
                    self.symboldf['range'] = self.symboldf['highPrice'] - self.symboldf['lowPrice']
                    self.symboldf['NR7'] = self.symboldf['range'].rolling(window=7).min().shift(1).fillna(0)
                    self.symboldf['NR4'] = self.symboldf['range'].rolling(window=4).min().shift(1).fillna(0)
                except:
                    pass
                self.outputdf = self.outputdf.append(self.symboldf.tail(1))
            df1 = self.outputdf[(self.outputdf['range'] <= self.outputdf['NR7']) & (self.outputdf['range']>0)]      
            outputdict = {"name":"narrowrange7","data":df1.to_json(orient='records',date_format='iso')}
            self.uploadtomongo(outputdict,{"name":"narrowrange7"})
            df2 = self.outputdf[(self.outputdf['range'] <= self.outputdf['NR4']) & (self.outputdf['range']>0)]      
            outputdict1 = {"name":"narrowrange4","data":df2.to_json(orient='records',date_format='iso')}
         #   self.coll.replace_one({"name":"narrowrange"},outputdict,True)  
            self.uploadtomongo(outputdict1,{"name":"narrowrange4"})
            #self.coll.update({"name":"narrowrange"},{"$set": outputdict},upsert=True)
    #        self.outputdf.to_csv(self.target+"_nr7.csv")       
        def uploadtomongo(self,output,nrtype):
            self.client = MongoClient('localhost',27017)
            self.db = self.client["StartofDay"]
            self.collection = self.db[self.target]     
            self.collection.remove(nrtype)
            self.collection.insert(output)
            self.client.close()
    
    
    
        def getNarrowRange7(self):
            df1 = pd.DataFrame()
            if (os.path.isfile(self.target+"_nr.csv")):
                df = pd.read_csv(self.target +"_nr.csv")
                df1 = df[(df['range'] <= df['NR7']) & (df['range']>0)]        
            return df1
        
    
        def getNarrowRange4(self):
            df1 = pd.DataFrame()
            if (os.path.isfile(self.target+"_nr.csv")):
                df = pd.read_csv(self.target +"_nr.csv")
                df1 = df[(df['range'] <= df['NR4']) & (df['range']>0)]        
            return df1