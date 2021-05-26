from DataFeed.SymbolFeed import EndofDayFeedSymbol
from DataFeed.Feed import EndofDayFeed
import json
import pandas as pd
import talib as tl
import os.path
from pymongo import MongoClient

class ImplementPattern(object):
    
    def __init__(self,target,noofdays):
        self.target = target
        self.masterlist = EndofDayFeedSymbol().getMaster()
        self.eodlist = EndofDayFeed().getData(target, noofdays)
        self.symboldf = pd.DataFrame()
        self.outputdf = pd.DataFrame()  
   

        
    def setPattern(self):
        data = self.masterlist
        symboldata = self.eodlist
        symbollist = data['master_symbol'].tolist()
        candle_names = tl.get_function_groups()['Pattern Recognition']
        for symbol in symbollist:
            print("Trying for symbol : " + symbol)
            try:
                self.symboldf = symboldata[(symboldata['symbol'] == symbol)]
                self.symboldf = self.symboldf.reset_index()
                for candle in candle_names:
                   self.symboldf['pattern'] = getattr(tl,candle)(self.symboldf['openPrice'].astype('float64'),self.symboldf['highPrice'].astype('float64'),self.symboldf['lowPrice'].astype('float64'),self.symboldf['closePrice'].astype('float64'))
                   self.symboldf.loc[self.symboldf['pattern'] !=0 ,'CandlePattern'] = candle
                   self.symboldf.loc[self.symboldf['pattern'] ==100 ,'PatternType'] = 'Bullish'
                   self.symboldf.loc[self.symboldf['pattern'] ==-100 ,'PatternType'] = 'Bearish'
                self.outputdf = self.outputdf.append(self.symboldf.tail(1))
                
            except:
                pass
        df1 = self.outputdf[(self.outputdf['PatternType'] == 'Bullish') | (self.outputdf['PatternType'] == 'Bearish')]     
        outputdict = {"name":"candles","data": df1.to_json(orient='records',date_format='iso')}
    #self.collection.replace_one({"name":"candles"},outputdict,True)  
        self.uploadtomongo(outputdict)
     #   self.outputdf.to_csv(self.target + ".csv")
        return self.outputdf
    
    def uploadtomongo(self,outputdict):
        self.client = MongoClient('localhost',27017)
        self.db = self.client["StartofDay"]
        self.collection = self.db[self.target]     
        self.collection.remove({"name":"candles"})
        self.collection.insert(outputdict)
    
    
    def getBullishPattern(self):
        if (os.path.isfile(self.target+".csv")):
            df = pd.read_csv(self.target +".csv")
            df1 = df[(df['PatternType'] == 'Bullish')]        
            return df1
        
    def getBearishPattern(self):
        if (os.path.isfile(self.target+".csv")):
            df = pd.read_csv(self.target +".csv")
            df1 = df[(df['PatternType'] == 'Bearish')]        
            return df1
    
  
        